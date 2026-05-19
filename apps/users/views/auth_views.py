"""
Smart Tourism — Auth Views
Login, Register, Logout, Password Change, Token Refresh
"""
import logging
import requests
from django.conf import settings
from django.core.mail import send_mail
from django.core.signing import BadSignature, SignatureExpired, TimestampSigner
from django.utils import timezone
from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.decorators import authentication_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken

from apps.users.models import User
from apps.users.serializers import (
    CustomTokenObtainPairSerializer,
    RegisterSerializer,
    ChangePasswordSerializer,
    UserDetailSerializer,
)
from smart_tourism.exceptions import success_response, error_response, created_response

logger = logging.getLogger(__name__)
email_verification_signer = TimestampSigner(salt="smart-tourism-email-verification")


def build_email_verification_url(request, user):
    token = email_verification_signer.sign(str(user.pk))
    frontend_url = getattr(settings, "FRONTEND_URL", "http://localhost:5173").rstrip("/")
    return f"{frontend_url}/verify-email?token={token}"


def send_verification_email(request, user):
    verification_url = build_email_verification_url(request, user)
    subject = "Verify your Smart Tourism account"
    message = (
        f"Hello {user.full_name},\n\n"
        "Please verify your Smart Tourism account using this link:\n"
        f"{verification_url}\n\n"
        "If you did not create this account, you can ignore this email."
    )
    sent = send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=True,
    )
    return verification_url, bool(sent)


class LoginView(TokenObtainPairView):
    """
    POST /api/v1/auth/login/
    Returns access + refresh tokens with user info.
    """
    permission_classes = [AllowAny]
    authentication_classes = []
    serializer_class   = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            return error_response("Invalid credentials. Please check your email and password.", status_code=status.HTTP_401_UNAUTHORIZED)

        data    = serializer.validated_data
        user    = serializer.user
        logger.info("User logged in: %s", user.email)

        return Response({
            'success':       True,
            'message':       'Login successful.',
            'access_token':  data['access'],
            'refresh_token': data['refresh'],
            'token_type':    'Bearer',
            'user':          data['user'],
        }, status=status.HTTP_200_OK)


class RegisterView(generics.CreateAPIView):
    """
    POST /api/v1/auth/register/
    Visitor self-registration.
    """
    permission_classes = [AllowAny]
    authentication_classes = []
    serializer_class   = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Generate tokens immediately
        refresh = RefreshToken.for_user(user)
        verification_url, email_sent = send_verification_email(request, user)
        logger.info("New visitor registered: %s", user.email)

        response_data = {
            'success':       True,
            'message':       'Registration successful. Please verify your email.',
            'access_token':  str(refresh.access_token),
            'refresh_token': str(refresh),
            'email_sent':    email_sent,
            'user':          UserDetailSerializer(user, context={'request': request}).data,
        }
        if settings.DEBUG:
            response_data['verification_url'] = verification_url

        return Response(response_data, status=status.HTTP_201_CREATED)


class VerifyEmailView(APIView):
    """
    POST /api/v1/auth/verify-email/
    Body: { "token": "signed-token" }
    """
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        token = request.data.get("token")
        if not token:
            return error_response("Verification token is required.")

        try:
            user_id = email_verification_signer.unsign(token, max_age=60 * 60 * 24)
            user = User.objects.get(pk=user_id)
        except SignatureExpired:
            return error_response("Verification link has expired.", status_code=status.HTTP_400_BAD_REQUEST)
        except (BadSignature, User.DoesNotExist):
            return error_response("Invalid verification token.", status_code=status.HTTP_400_BAD_REQUEST)

        user.is_verified = True
        user.email_verified_at = timezone.now()
        user.save(update_fields=["is_verified", "email_verified_at", "updated_at"])
        return success_response(
            data=UserDetailSerializer(user, context={"request": request}).data,
            message="Email verified successfully.",
        )


class ResendVerificationEmailView(APIView):
    """
    POST /api/v1/auth/resend-verification/
    Sends another verification link to the logged-in user.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.user.is_verified:
            return success_response(message="Your email is already verified.")

        verification_url, email_sent = send_verification_email(request, request.user)
        data = {"email_sent": email_sent}
        if settings.DEBUG:
            data["verification_url"] = verification_url
        return success_response(data=data, message="Verification email sent.")


class GoogleLoginView(APIView):
    """
    POST /api/v1/auth/google/
    Body: { "credential": "google-id-token", "role": "visitor|admin" }
    """
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        credential = request.data.get("credential")
        requested_role = request.data.get("role", "visitor")
        if requested_role not in {"visitor", "admin"}:
            requested_role = "visitor"

        if not credential:
            return error_response("Google credential is required.")

        try:
            google_response = requests.get(
                "https://oauth2.googleapis.com/tokeninfo",
                params={"id_token": credential},
                timeout=8,
            )
            google_response.raise_for_status()
            profile = google_response.json()
        except requests.RequestException as exc:
            logger.warning("Google token verification failed: %s", exc)
            return error_response("Could not verify Google account.", status_code=status.HTTP_401_UNAUTHORIZED)

        client_id = getattr(settings, "GOOGLE_CLIENT_ID", "")
        if client_id and profile.get("aud") != client_id:
            return error_response("Google token audience does not match this app.", status_code=status.HTTP_401_UNAUTHORIZED)

        email = profile.get("email")
        if not email or profile.get("email_verified") not in ("true", True):
            return error_response("Google email is not verified.", status_code=status.HTTP_401_UNAUTHORIZED)

        first_name = profile.get("given_name", "")
        last_name = profile.get("family_name", "")
        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                "username": email,
                "first_name": first_name,
                "last_name": last_name,
                "role": requested_role,
                "is_verified": True,
                "email_verified_at": timezone.now(),
            },
        )

        if created:
            from apps.users.models import VisitorProfile
            if user.role == "visitor":
                VisitorProfile.objects.get_or_create(user=user)
            user.set_unusable_password()
            user.save()
        elif not user.is_verified:
            user.is_verified = True
            user.email_verified_at = timezone.now()
            user.save(update_fields=["is_verified", "email_verified_at", "updated_at"])

        refresh = RefreshToken.for_user(user)
        return Response({
            "success": True,
            "message": "Google login successful.",
            "access_token": str(refresh.access_token),
            "refresh_token": str(refresh),
            "token_type": "Bearer",
            "user": UserDetailSerializer(user, context={"request": request}).data,
        }, status=status.HTTP_200_OK)


class LogoutView(APIView):
    """
    POST /api/v1/auth/logout/
    Blacklists the refresh token.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get('refresh_token')
            if not refresh_token:
                return error_response("refresh_token is required.")
            token = RefreshToken(refresh_token)
            token.blacklist()
            logger.info("User logged out: %s", request.user.email)
            return success_response(message="Logged out successfully.")
        except TokenError as e:
            return error_response(str(e))


class TokenRefreshCustomView(TokenRefreshView):
    """
    POST /api/v1/auth/token/refresh/
    Standard DRF-SimpleJWT refresh with consistent envelope.
    """
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            return Response({
                'success':      True,
                'access_token': response.data['access'],
            }, status=status.HTTP_200_OK)
        return response


class ChangePasswordView(APIView):
    """
    POST /api/v1/auth/change-password/
    Authenticated user changes own password.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user
        if not user.check_password(serializer.validated_data['old_password']):
            return error_response("Old password is incorrect.")

        user.set_password(serializer.validated_data['new_password'])
        user.save()
        logger.info("Password changed for user: %s", user.email)
        return success_response(message="Password updated successfully.")


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def me(request):
    """
    GET /api/v1/auth/me/
    Returns the currently authenticated user's profile.
    """
    serializer = UserDetailSerializer(request.user, context={'request': request})
    return success_response(data=serializer.data)

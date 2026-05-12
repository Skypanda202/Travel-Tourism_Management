"""
Smart Tourism — Auth Views
Login, Register, Logout, Password Change, Token Refresh
"""
import logging
from django.utils import timezone
from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
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


class LoginView(TokenObtainPairView):
    """
    POST /api/v1/auth/login/
    Returns access + refresh tokens with user info.
    """
    permission_classes = [AllowAny]
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
    serializer_class   = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Generate tokens immediately
        refresh = RefreshToken.for_user(user)
        logger.info("New visitor registered: %s", user.email)

        return Response({
            'success':       True,
            'message':       'Registration successful. Welcome!',
            'access_token':  str(refresh.access_token),
            'refresh_token': str(refresh),
            'user':          UserDetailSerializer(user, context={'request': request}).data,
        }, status=status.HTTP_201_CREATED)


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
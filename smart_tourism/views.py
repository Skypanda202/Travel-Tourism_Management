from django.contrib.auth import get_user_model
from django.conf import settings

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from apps.users.models import VisitorProfile
from apps.users.views.auth_views import send_verification_email

@api_view(["POST"])
@permission_classes([AllowAny])
def register(request):
    User = get_user_model()

    name = (request.data.get("name") or "").strip()
    email = request.data.get("email")
    password = request.data.get("password")

    if not email or not password:
        return Response(
            {"error": "Email and password are required"},
            status=400
        )

    # Check existing user
    if User.objects.filter(email=email).exists():
        return Response(
            {"error": "User already exists"},
            status=400
        )

    name_parts = name.split(maxsplit=1)
    first_name = name_parts[0] if name_parts else ""
    last_name = name_parts[1] if len(name_parts) > 1 else ""

    # Create user
    user = User.objects.create_user(
        username=email,
        email=email,
        password=password,
        first_name=first_name,
        last_name=last_name,
        role="visitor",
    )

    VisitorProfile.objects.get_or_create(user=user)
    verification_url, email_sent = send_verification_email(request, user)

    data = {
        "message": "User registered successfully. Please verify your email.",
        "email_sent": email_sent,
    }
    if settings.DEBUG:
        data["verification_url"] = verification_url

    return Response(data, status=201)

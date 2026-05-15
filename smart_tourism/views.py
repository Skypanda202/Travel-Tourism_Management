from django.contrib.auth import get_user_model

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from apps.users.models import VisitorProfile

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

    return Response({
        "message": "User registered successfully"
    }, status=201)

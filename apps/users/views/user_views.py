"""
Smart Tourism — User Management Views
Admin: CRUD on users; Visitor: own profile
"""
import logging
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.users.models import User, VisitorProfile
from apps.users.serializers import (
    UserListSerializer,
    UserDetailSerializer,
    UserUpdateSerializer,
    VisitorProfileSerializer,
    AdminUserSerializer,
)
from smart_tourism.permissions import IsAdmin, IsOwnerOrAdmin
from smart_tourism.exceptions import success_response, error_response
from smart_tourism.pagination import StandardResultsPagination

logger = logging.getLogger(__name__)


class UserViewSet(viewsets.ModelViewSet):
    """
    Admin-facing user management.
    GET    /api/v1/users/          — list all users
    POST   /api/v1/users/          — create user
    GET    /api/v1/users/{id}/     — user detail
    PUT    /api/v1/users/{id}/     — full update
    PATCH  /api/v1/users/{id}/     — partial update
    DELETE /api/v1/users/{id}/     — deactivate user
    GET    /api/v1/users/{id}/bookings/  — user's bookings (admin)
    POST   /api/v1/users/{id}/activate/ — activate user
    POST   /api/v1/users/{id}/deactivate/ — deactivate user
    """
    queryset           = User.objects.all().order_by('-created_at')
    permission_classes = [IsAdmin]
    pagination_class   = StandardResultsPagination
    filter_backends    = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields   = ['role', 'is_active', 'is_verified', 'country', 'city']
    search_fields      = ['email', 'username', 'first_name', 'last_name', 'phone_number']
    ordering_fields    = ['created_at', 'email', 'last_login']

    def get_serializer_class(self):
        if self.action == 'list':
            return UserListSerializer
        if self.action in ['create', 'update', 'partial_update']:
            return AdminUserSerializer
        return UserDetailSerializer

    def destroy(self, request, *args, **kwargs):
        """Soft-delete: deactivate instead of hard delete."""
        user = self.get_object()
        user.is_active = False
        user.save()
        logger.info("Admin %s deactivated user %s", request.user.email, user.email)
        return success_response(message=f"User {user.email} has been deactivated.")

    @action(detail=True, methods=['post'])
    def activate(self, request, pk=None):
        user = self.get_object()
        user.is_active = True
        user.save()
        return success_response(message=f"User {user.email} activated.")

    @action(detail=True, methods=['post'])
    def deactivate(self, request, pk=None):
        user = self.get_object()
        user.is_active = False
        user.save()
        return success_response(message=f"User {user.email} deactivated.")

    @action(detail=True, methods=['get'])
    def bookings(self, request, pk=None):
        """Return a user's booking history (admin view)."""
        from apps.bookings.models import Booking
        from apps.bookings.serializers import BookingListSerializer
        user     = self.get_object()
        bookings = Booking.objects.filter(visitor=user).order_by('-created_at')
        serializer = BookingListSerializer(bookings, many=True, context={'request': request})
        return success_response(data=serializer.data)

    @action(detail=True, methods=['get'])
    def activity(self, request, pk=None):
        """Return visitor tracking activities for this user."""
        from apps.analytics.models import VisitorActivity
        user       = self.get_object()
        activities = VisitorActivity.objects.filter(user=user).order_by('-created_at')[:50]
        data = [{'action': a.action, 'resource': a.resource_type, 'timestamp': a.created_at} for a in activities]
        return success_response(data=data)


class VisitorProfileViewSet(viewsets.GenericViewSet):
    """
    Visitor profile endpoints (own profile only).
    GET   /api/v1/users/profile/        — get own profile
    PATCH /api/v1/users/profile/        — update own profile
    GET   /api/v1/users/visitor-profile/— visitor-specific preferences
    PATCH /api/v1/users/visitor-profile/— update visitor preferences
    """
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get', 'patch'])
    def profile(self, request):
        user = request.user
        if request.method == 'GET':
            serializer = UserDetailSerializer(user, context={'request': request})
            return success_response(data=serializer.data)

        serializer = UserUpdateSerializer(user, data=request.data, partial=True, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return success_response(
            data=UserDetailSerializer(user, context={'request': request}).data,
            message="Profile updated successfully."
        )

    @action(detail=False, methods=['get', 'patch'], url_path='visitor-profile')
    def visitor_profile(self, request):
        try:
            vp = request.user.visitor_profile
        except VisitorProfile.DoesNotExist:
            vp = VisitorProfile.objects.create(user=request.user)

        if request.method == 'GET':
            return success_response(data=VisitorProfileSerializer(vp).data)

        serializer = VisitorProfileSerializer(vp, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return success_response(data=serializer.data, message="Visitor profile updated.")

    @action(detail=False, methods=['get'])
    def favorites(self, request):
        """Get visitor's saved favourite places."""
        from apps.places.models import Favorite
        from apps.places.serializers import FavoriteSerializer
        favs = Favorite.objects.filter(user=request.user).select_related('place')
        serializer = FavoriteSerializer(favs, many=True, context={'request': request})
        return success_response(data=serializer.data)

    @action(detail=False, methods=['get'])
    def dashboard(self, request):
        """Quick stats for visitor dashboard."""
        from apps.bookings.models import Booking
        from apps.reviews.models import Review
        from apps.places.models import Favorite
        user  = request.user
        stats = {
            'total_bookings':    Booking.objects.filter(visitor=user).count(),
            'upcoming_bookings': Booking.objects.filter(visitor=user, status='confirmed').count(),
            'total_reviews':     Review.objects.filter(user=user).count(),
            'saved_places':      Favorite.objects.filter(user=user).count(),
        }
        return success_response(data=stats)

    @action(detail=False, methods=['delete'], url_path='delete-account')
    def delete_account(self, request):
        """Authenticated users can deactivate their own account."""
        user = request.user
        user.is_active = False
        user.save(update_fields=['is_active', 'updated_at'])
        logger.info("User self-deleted account: %s", user.email)
        return success_response(message="Your account has been deactivated.")

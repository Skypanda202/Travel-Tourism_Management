"""Smart Tourism — Bookings Views."""
import logging
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from apps.bookings.models import Booking
from apps.bookings.serializers import (
    BookingCreateSerializer,
    BookingListSerializer,
    BookingDetailSerializer,
    BookingStatusUpdateSerializer,
    BookingCancelSerializer,
)
from apps.places.models import TouristPlace
from smart_tourism.exceptions import success_response, error_response
from smart_tourism.pagination import StandardResultsPagination
from smart_tourism.permissions import IsAdmin, IsOwnerOrAdmin

logger = logging.getLogger(__name__)


class BookingViewSet(viewsets.ModelViewSet):
    """
    Bookings API.
    Visitors see only their own. Admins see all.
    """
    permission_classes = [IsAuthenticated]
    pagination_class   = StandardResultsPagination
    filter_backends    = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields   = ['status', 'payment_status', 'place']
    search_fields      = ['booking_ref', 'visitor__email', 'place__name']
    ordering_fields    = ['created_at', 'visit_date', 'total_amount']

    def get_queryset(self):
        user = self.request.user
        qs   = Booking.objects.select_related('visitor', 'place')
        if user.is_admin:
            return qs.all()
        return qs.filter(visitor=user)

    def get_serializer_class(self):
        if self.action == 'create':
            return BookingCreateSerializer
        if self.action == 'list':
            return BookingListSerializer
        if self.action in ['update_status']:
            return BookingStatusUpdateSerializer
        return BookingDetailSerializer

    def perform_create(self, serializer):
        place = serializer.validated_data['place']
        # Price calculation
        adult_fee    = place.entry_fee
        children_fee = adult_fee * 0.5    # 50% for children
        num_adults   = serializer.validated_data.get('num_adults', 1)
        num_children = serializer.validated_data.get('num_children', 0)
        total        = (adult_fee * num_adults) + (children_fee * num_children)

        booking = serializer.save(
            visitor=self.request.user,
            adult_fee=adult_fee,
            children_fee=children_fee,
            total_amount=total,
        )
        # Update place bookings count
        TouristPlace.objects.filter(pk=place.pk).update(
            total_bookings=place.total_bookings + 1
        )
        logger.info("Booking %s created by %s", booking.booking_ref, self.request.user.email)

    def perform_destroy(self, instance):
        """Soft cancel instead of hard delete."""
        instance.status      = 'cancelled'
        instance.cancelled_at = timezone.now()
        instance.save()

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """POST /api/v1/bookings/{id}/cancel/"""
        booking = self.get_object()
        if booking.visitor != request.user and not request.user.is_admin:
            return error_response("Not authorised.", status_code=status.HTTP_403_FORBIDDEN)
        if booking.status in ['cancelled', 'completed']:
            return error_response(f"Booking is already {booking.status}.")

        serializer = BookingCancelSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        booking.status       = 'cancelled'
        booking.cancelled_at = timezone.now()
        booking.cancel_reason = serializer.validated_data.get('cancel_reason', '')
        booking.save()
        return success_response(message="Booking cancelled successfully.")

    @action(detail=True, methods=['patch'], permission_classes=[IsAdmin])
    def update_status(self, request, pk=None):
        """PATCH /api/v1/bookings/{id}/update-status/ — admin only."""
        booking    = self.get_object()
        serializer = BookingStatusUpdateSerializer(booking, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return success_response(
            data=BookingDetailSerializer(booking).data,
            message="Booking status updated."
        )

    @action(detail=False, methods=['get'], permission_classes=[IsAdmin])
    def stats(self, request):
        """GET /api/v1/bookings/stats/ — admin booking statistics."""
        from django.db.models import Sum, Count
        qs    = Booking.objects.all()
        stats = {
            'total':     qs.count(),
            'pending':   qs.filter(status='pending').count(),
            'confirmed': qs.filter(status='confirmed').count(),
            'completed': qs.filter(status='completed').count(),
            'cancelled': qs.filter(status='cancelled').count(),
            'revenue':   qs.filter(payment_status='paid').aggregate(total=Sum('total_amount'))['total'] or 0,
        }
        return success_response(data=stats)
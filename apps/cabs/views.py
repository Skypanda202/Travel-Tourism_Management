"""Smart Tourism — Cabs Views."""
import logging
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny

from apps.cabs.models import CabType, CabBooking
from apps.cabs.serializers import (
    CabTypeSerializer,
    CabBookingCreateSerializer,
    CabBookingListSerializer,
    CabBookingDetailSerializer,
)
from smart_tourism.exceptions import success_response, error_response
from smart_tourism.pagination import StandardResultsPagination
from smart_tourism.permissions import IsAdmin, IsAdminOrReadOnly

logger = logging.getLogger(__name__)


class CabTypeViewSet(viewsets.ModelViewSet):
    """CRUD for cab types (public read, admin write)."""
    queryset           = CabType.objects.filter(is_available=True)
    serializer_class   = CabTypeSerializer
    permission_classes = [IsAdminOrReadOnly]


class CabBookingViewSet(viewsets.ModelViewSet):
    """Cab booking management."""
    permission_classes = [IsAuthenticated]
    pagination_class   = StandardResultsPagination

    def get_queryset(self):
        user = self.request.user
        qs   = CabBooking.objects.select_related('visitor', 'cab_type')
        if user.is_admin:
            return qs.all()
        return qs.filter(visitor=user)

    def get_serializer_class(self):
        if self.action == 'create':
            return CabBookingCreateSerializer
        if self.action == 'list':
            return CabBookingListSerializer
        return CabBookingDetailSerializer

    def perform_create(self, serializer):
        cab_type    = serializer.validated_data['cab_type']
        dist        = serializer.validated_data.get('distance_km', 0) or 0
        dist_fare   = cab_type.price_per_km * dist
        total       = cab_type.base_fare + dist_fare
        booking = serializer.save(
            visitor=self.request.user,
            base_fare=cab_type.base_fare,
            distance_fare=dist_fare,
            total_fare=total,
        )
        logger.info("Cab booking %s created", booking.booking_ref)

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        booking = self.get_object()
        if booking.visitor != request.user and not request.user.is_admin:
            return error_response("Not authorised.", status_code=status.HTTP_403_FORBIDDEN)
        if booking.status in ['cancelled', 'completed']:
            return error_response(f"Booking already {booking.status}.")
        booking.status = 'cancelled'
        booking.save()
        return success_response(message="Cab booking cancelled.")

    @action(detail=True, methods=['patch'], permission_classes=[IsAdmin])
    def assign_driver(self, request, pk=None):
        """Admin assigns a driver to a cab booking."""
        booking = self.get_object()
        booking.driver_name    = request.data.get('driver_name', '')
        booking.driver_phone   = request.data.get('driver_phone', '')
        booking.vehicle_number = request.data.get('vehicle_number', '')
        booking.status         = 'confirmed'
        booking.save()
        return success_response(message="Driver assigned.", data=CabBookingDetailSerializer(booking).data)

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def estimate_fare(self, request):
        """
        POST /api/v1/cabs/estimate-fare/
        Body: { cab_type_id, distance_km }
        """
        try:
            cab_type_id = request.data['cab_type_id']
            distance_km = float(request.data['distance_km'])
        except (KeyError, ValueError):
            return error_response("Provide cab_type_id and distance_km.")

        try:
            cab = CabType.objects.get(pk=cab_type_id, is_available=True)
        except CabType.DoesNotExist:
            return error_response("Cab type not found.")

        dist_fare  = cab.price_per_km * distance_km
        total_fare = cab.base_fare + dist_fare

        return success_response(data={
            'cab_type':     cab.name,
            'base_fare':    float(cab.base_fare),
            'distance_fare': round(float(dist_fare), 2),
            'total_fare':   round(float(total_fare), 2),
            'currency':     'INR',
        })
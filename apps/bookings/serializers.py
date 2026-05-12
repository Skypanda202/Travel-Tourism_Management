"""Smart Tourism — Bookings Serializers."""
from rest_framework import serializers
from django.utils import timezone
from apps.bookings.models import Booking
from apps.places.serializers import TouristPlaceListSerializer
from apps.users.serializers import UserListSerializer


class BookingCreateSerializer(serializers.ModelSerializer):
    """Visitor creates a new booking."""
    class Meta:
        model  = Booking
        fields = [
            'id', 'place', 'visit_date', 'num_adults', 'num_children',
            'special_notes', 'currency',
        ]

    def validate_visit_date(self, value):
        if value < timezone.now().date():
            raise serializers.ValidationError("Visit date cannot be in the past.")
        return value

    def validate_num_adults(self, value):
        if value < 1:
            raise serializers.ValidationError("At least 1 adult is required.")
        return value


class BookingListSerializer(serializers.ModelSerializer):
    """Compact booking for lists."""
    place_name    = serializers.CharField(source='place.name', read_only=True)
    place_city    = serializers.CharField(source='place.city', read_only=True)
    visitor_email = serializers.CharField(source='visitor.email', read_only=True)
    visitor_name  = serializers.CharField(source='visitor.full_name', read_only=True)

    class Meta:
        model  = Booking
        fields = [
            'id', 'booking_ref', 'place', 'place_name', 'place_city',
            'visitor_email', 'visitor_name', 'visit_date',
            'num_adults', 'num_children', 'total_amount', 'currency',
            'status', 'payment_status', 'created_at',
        ]


class BookingDetailSerializer(serializers.ModelSerializer):
    """Full booking detail."""
    place   = TouristPlaceListSerializer(read_only=True)
    visitor = UserListSerializer(read_only=True)

    class Meta:
        model  = Booking
        fields = '__all__'
        read_only_fields = ['id', 'booking_ref', 'created_at', 'updated_at']


class BookingStatusUpdateSerializer(serializers.ModelSerializer):
    """Admin updates booking status."""
    class Meta:
        model  = Booking
        fields = ['status', 'payment_status']


class BookingCancelSerializer(serializers.Serializer):
    cancel_reason = serializers.CharField(required=False, allow_blank=True)
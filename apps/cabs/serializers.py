"""Smart Tourism — Cabs Serializers."""
from rest_framework import serializers
from django.utils import timezone
from apps.cabs.models import CabType, CabBooking


class CabTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model  = CabType
        fields = '__all__'


class CabBookingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model  = CabBooking
        fields = [
            'cab_type', 'pickup_address', 'pickup_latitude', 'pickup_longitude',
            'dropoff_address', 'dropoff_latitude', 'dropoff_longitude',
            'distance_km', 'pickup_datetime', 'num_passengers', 'special_requests',
        ]

    def validate_pickup_datetime(self, value):
        if value < timezone.now():
            raise serializers.ValidationError("Pickup time cannot be in the past.")
        return value


class CabBookingListSerializer(serializers.ModelSerializer):
    cab_type_name = serializers.CharField(source='cab_type.name', read_only=True)
    visitor_email = serializers.CharField(source='visitor.email', read_only=True)

    class Meta:
        model  = CabBooking
        fields = [
            'id', 'booking_ref', 'cab_type', 'cab_type_name', 'visitor_email',
            'pickup_address', 'dropoff_address', 'pickup_datetime',
            'total_fare', 'status', 'payment_status', 'created_at',
        ]


class CabBookingDetailSerializer(serializers.ModelSerializer):
    cab_type = CabTypeSerializer(read_only=True)

    class Meta:
        model  = CabBooking
        fields = '__all__'
        read_only_fields = ['id', 'booking_ref', 'created_at', 'updated_at']
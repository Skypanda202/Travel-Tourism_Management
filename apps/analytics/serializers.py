"""Smart Tourism — Analytics Serializers."""
from rest_framework import serializers
from apps.analytics.models import DailyAnalytics, PlaceAnalytics, VisitorActivity


class DailyAnalyticsSerializer(serializers.ModelSerializer):
    class Meta:
        model  = DailyAnalytics
        fields = '__all__'


class PlaceAnalyticsSerializer(serializers.ModelSerializer):
    place_name = serializers.CharField(source='place.name', read_only=True)

    class Meta:
        model  = PlaceAnalytics
        fields = ['id', 'place', 'place_name', 'date', 'views',
                'bookings', 'favorites', 'reviews', 'revenue']


class VisitorActivitySerializer(serializers.ModelSerializer):
    user_email = serializers.CharField(source='user.email', read_only=True)

    class Meta:
        model  = VisitorActivity
        fields = ['id', 'user', 'user_email', 'action', 'resource_type',
                'resource_id', 'resource_name', 'ip_address', 'extra_data', 'created_at']
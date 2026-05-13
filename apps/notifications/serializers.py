"""Smart Tourism — Notifications Serializers."""
from rest_framework import serializers
from apps.notifications.models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Notification
        fields = ['id', 'type', 'title', 'message', 'is_read', 'data', 'created_at', 'read_at']
        read_only_fields = ['id', 'created_at', 'read_at']


class BroadcastNotificationSerializer(serializers.Serializer):
    """Admin broadcasts to all users or a specific role."""
    title   = serializers.CharField(max_length=255)
    message = serializers.CharField()
    type    = serializers.ChoiceField(choices=['system', 'promo'])
    role    = serializers.ChoiceField(choices=['all', 'visitor', 'admin'], default='visitor')
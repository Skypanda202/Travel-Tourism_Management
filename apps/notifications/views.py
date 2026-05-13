"""Smart Tourism — Notifications Views."""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from apps.notifications.models import Notification
from apps.notifications.serializers import NotificationSerializer, BroadcastNotificationSerializer
from smart_tourism.exceptions import success_response, error_response
from smart_tourism.pagination import StandardResultsPagination
from smart_tourism.permissions import IsAdmin


class NotificationViewSet(viewsets.GenericViewSet):
    """
    GET  /api/v1/notifications/            — list own notifications
    POST /api/v1/notifications/mark-read/  — mark one or all as read
    GET  /api/v1/notifications/unread-count/ — badge count
    POST /api/v1/notifications/broadcast/  — admin: send to role (admin only)
    DELETE /api/v1/notifications/clear/    — delete all own notifications
    """
    permission_classes = [IsAuthenticated]
    pagination_class   = StandardResultsPagination

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)

    @action(detail=False, methods=['get'])
    def list_notifications(self, request):
        qs = self.get_queryset()
        unread_only = request.query_params.get('unread')
        if unread_only:
            qs = qs.filter(is_read=False)
        page = self.paginate_queryset(qs)
        if page is not None:
            return self.get_paginated_response(NotificationSerializer(page, many=True).data)
        return success_response(data=NotificationSerializer(qs, many=True).data)

    @action(detail=False, methods=['post'], url_path='mark-read')
    def mark_read(self, request):
        """
        POST /api/v1/notifications/mark-read/
        Body: { "id": 5 }  or  { "all": true }
        """
        if request.data.get('all'):
            self.get_queryset().filter(is_read=False).update(is_read=True)
            return success_response(message="All notifications marked as read.")

        notif_id = request.data.get('id')
        if not notif_id:
            return error_response("Provide 'id' or 'all': true.")
        try:
            notif = self.get_queryset().get(pk=notif_id)
            notif.mark_read()
            return success_response(message="Notification marked as read.")
        except Notification.DoesNotExist:
            return error_response("Notification not found.", status_code=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['get'], url_path='unread-count')
    def unread_count(self, request):
        count = self.get_queryset().filter(is_read=False).count()
        return success_response(data={'unread_count': count})

    @action(detail=False, methods=['delete'])
    def clear(self, request):
        self.get_queryset().delete()
        return success_response(message="All notifications cleared.")

    @action(detail=False, methods=['post'], permission_classes=[IsAdmin])
    def broadcast(self, request):
        """Admin broadcasts a notification to all users of a given role."""
        from apps.users.models import User
        serializer = BroadcastNotificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        users = User.objects.filter(is_active=True)
        if data['role'] != 'all':
            users = users.filter(role=data['role'])

        notifications = [
            Notification(
                user=u,
                type=data['type'],
                title=data['title'],
                message=data['message'],
            )
            for u in users
        ]
        Notification.objects.bulk_create(notifications, batch_size=500)
        return success_response(message=f"Broadcast sent to {len(notifications)} users.")
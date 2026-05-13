from django.urls import path
from apps.notifications.views import NotificationViewSet

notif = NotificationViewSet.as_view

urlpatterns = [
    path('',              notif({'get': 'list_notifications'}), name='notifications-list'),
    path('mark-read/',    notif({'post': 'mark_read'}),         name='notifications-mark-read'),
    path('unread-count/', notif({'get': 'unread_count'}),       name='notifications-unread'),
    path('broadcast/',    notif({'post': 'broadcast'}),         name='notifications-broadcast'),
    path('clear/',        notif({'delete': 'clear'}),           name='notifications-clear'),
]
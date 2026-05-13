from django.contrib import admin
from apps.analytics.models import DailyAnalytics, PlaceAnalytics, VisitorActivity


@admin.register(DailyAnalytics)
class DailyAnalyticsAdmin(admin.ModelAdmin):
    list_display  = ['date', 'total_visits', 'unique_visitors', 'total_bookings',
                    'cab_bookings', 'total_revenue', 'new_registrations']
    list_filter   = ['date']
    ordering      = ['-date']
    readonly_fields = [f.name for f in DailyAnalytics._meta.fields]   # all read-only in admin


@admin.register(PlaceAnalytics)
class PlaceAnalyticsAdmin(admin.ModelAdmin):
    list_display  = ['place', 'date', 'views', 'bookings', 'reviews', 'revenue']
    list_filter   = ['date']
    raw_id_fields = ['place']
    ordering      = ['-date']


@admin.register(VisitorActivity)
class VisitorActivityAdmin(admin.ModelAdmin):
    list_display  = ['user', 'action', 'resource_type', 'resource_name', 'ip_address', 'created_at']
    list_filter   = ['action', 'resource_type']
    search_fields = ['user__email', 'resource_name', 'ip_address']
    raw_id_fields = ['user']
    readonly_fields = [f.name for f in VisitorActivity._meta.fields]
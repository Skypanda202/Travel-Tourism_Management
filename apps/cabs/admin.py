from django.contrib import admin
from apps.cabs.models import CabType, CabBooking


@admin.register(CabType)
class CabTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'capacity', 'price_per_km', 'base_fare', 'is_ac', 'is_available']
    list_filter  = ['is_ac', 'is_available']


@admin.register(CabBooking)
class CabBookingAdmin(admin.ModelAdmin):
    list_display  = ['booking_ref', 'visitor', 'cab_type', 'pickup_datetime', 'total_fare', 'status', 'payment_status']
    list_filter   = ['status', 'payment_status']
    search_fields = ['booking_ref', 'visitor__email']
    raw_id_fields = ['visitor']
from django.contrib import admin
from apps.bookings.models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display  = ['booking_ref', 'visitor', 'place', 'visit_date', 'total_amount', 'status', 'payment_status', 'created_at']
    list_filter   = ['status', 'payment_status', 'created_at']
    search_fields = ['booking_ref', 'visitor__email', 'place__name']
    raw_id_fields = ['visitor', 'place']
    readonly_fields = ['booking_ref', 'created_at', 'updated_at', 'cancelled_at']
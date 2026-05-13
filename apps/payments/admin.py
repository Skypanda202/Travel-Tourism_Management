from django.contrib import admin
from apps.payments.models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display   = ['transaction_ref', 'user', 'payment_type', 'amount', 'currency',
                    'payment_method', 'status', 'initiated_at', 'completed_at']
    list_filter    = ['status', 'payment_method', 'payment_type', 'currency']
    search_fields  = ['transaction_ref', 'user__email', 'gateway_payment_id']
    raw_id_fields  = ['user']
    readonly_fields = ['transaction_ref', 'initiated_at', 'completed_at', 'refunded_at']
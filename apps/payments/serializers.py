"""Smart Tourism — Payments Serializers."""
from rest_framework import serializers
from apps.payments.models import Payment


class PaymentListSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Payment
        fields = [
            'id', 'transaction_ref', 'payment_type', 'booking_id',
            'amount', 'currency', 'net_amount', 'payment_method',
            'status', 'initiated_at', 'completed_at',
        ]


class PaymentDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Payment
        fields = '__all__'
        read_only_fields = ['id', 'transaction_ref', 'initiated_at']


class PaymentInitiateSerializer(serializers.Serializer):
    """Initiate a payment for a booking."""
    payment_type   = serializers.ChoiceField(choices=['booking', 'cab_booking'])
    booking_id     = serializers.IntegerField()
    payment_method = serializers.ChoiceField(choices=['card', 'upi', 'netbanking', 'wallet', 'cash'])
    gateway        = serializers.CharField(max_length=50, default='razorpay')


class PaymentVerifySerializer(serializers.Serializer):
    """Verify gateway callback."""
    transaction_ref    = serializers.CharField()
    gateway_payment_id = serializers.CharField()
    gateway_signature  = serializers.CharField(required=False)
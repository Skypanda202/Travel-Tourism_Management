"""Smart Tourism — Payments Views."""
import logging
from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from apps.payments.models import Payment
from apps.payments.serializers import (
    PaymentListSerializer,
    PaymentDetailSerializer,
    PaymentInitiateSerializer,
    PaymentVerifySerializer,
)
from smart_tourism.exceptions import success_response, error_response
from smart_tourism.pagination import StandardResultsPagination
from smart_tourism.permissions import IsAdmin

logger = logging.getLogger(__name__)


class PaymentViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Payments API (read + initiate + verify).
    GET  /api/v1/payments/           — list own payments
    GET  /api/v1/payments/{id}/      — detail
    POST /api/v1/payments/initiate/  — start a payment
    POST /api/v1/payments/verify/    — verify gateway callback
    GET  /api/v1/payments/revenue/   — admin revenue summary
    """
    permission_classes = [IsAuthenticated]
    pagination_class   = StandardResultsPagination

    def get_queryset(self):
        user = self.request.user
        qs   = Payment.objects.all()
        if not user.is_admin:
            qs = qs.filter(user=user)
        return qs

    def get_serializer_class(self):
        if self.action == 'list':
            return PaymentListSerializer
        return PaymentDetailSerializer

    @action(detail=False, methods=['post'])
    def initiate(self, request):
        """Initiate payment → create Payment record → return gateway order details."""
        serializer = PaymentInitiateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        # Resolve amount from booking
        amount = self._get_booking_amount(data['payment_type'], data['booking_id'])
        if amount is None:
            return error_response("Booking not found or already paid.")

        payment = Payment.objects.create(
            user=request.user,
            payment_type=data['payment_type'],
            booking_id=data['booking_id'],
            amount=amount,
            payment_method=data['payment_method'],
            gateway=data.get('gateway', 'razorpay'),
            status='pending',
        )

        # In production: call Razorpay/Stripe SDK to get gateway order id
        # For now we mock the gateway response
        gateway_data = {
            'transaction_ref': payment.transaction_ref,
            'amount':          float(payment.net_amount),
            'currency':        payment.currency,
            'gateway':         payment.gateway,
            # 'gateway_order_id': razorpay_order.id   ← real integration
        }
        logger.info("Payment initiated: %s for user %s", payment.transaction_ref, request.user.email)
        return success_response(data=gateway_data, message="Payment initiated.")

    @action(detail=False, methods=['post'])
    def verify(self, request):
        """Verify payment after gateway callback."""
        serializer = PaymentVerifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        try:
            payment = Payment.objects.get(transaction_ref=data['transaction_ref'], user=request.user)
        except Payment.DoesNotExist:
            return error_response("Payment record not found.")

        # In production: verify signature with gateway SDK
        payment.gateway_payment_id = data['gateway_payment_id']
        payment.gateway_signature  = data.get('gateway_signature', '')
        payment.status             = 'success'
        payment.completed_at       = timezone.now()
        payment.save()

        # Mark booking as paid
        self._mark_booking_paid(payment)

        logger.info("Payment verified: %s", payment.transaction_ref)
        return success_response(message="Payment successful.", data=PaymentDetailSerializer(payment).data)

    @action(detail=False, methods=['get'], permission_classes=[IsAdmin])
    def revenue(self, request):
        """GET /api/v1/payments/revenue/ — admin revenue dashboard."""
        from django.db.models import Sum, Count
        from django.utils.timezone import now
        from datetime import timedelta

        qs = Payment.objects.filter(status='success')

        today    = now().date()
        month_start = today.replace(day=1)
        year_start  = today.replace(month=1, day=1)

        stats = {
            'total_revenue':       float(qs.aggregate(t=Sum('net_amount'))['t'] or 0),
            'today_revenue':       float(qs.filter(completed_at__date=today).aggregate(t=Sum('net_amount'))['t'] or 0),
            'this_month_revenue':  float(qs.filter(completed_at__date__gte=month_start).aggregate(t=Sum('net_amount'))['t'] or 0),
            'this_year_revenue':   float(qs.filter(completed_at__date__gte=year_start).aggregate(t=Sum('net_amount'))['t'] or 0),
            'total_transactions':  qs.count(),
            'by_method': list(
                qs.values('payment_method').annotate(
                    count=Count('id'), amount=Sum('net_amount')
                )
            ),
        }
        return success_response(data=stats)

    # ── Helpers ───────────────────────────────────────────────────────────────

    def _get_booking_amount(self, payment_type, booking_id):
        try:
            if payment_type == 'booking':
                from apps.bookings.models import Booking
                b = Booking.objects.get(pk=booking_id, visitor=self.request.user)
                if b.payment_status == 'paid':
                    return None
                return b.total_amount
            else:
                from apps.cabs.models import CabBooking
                b = CabBooking.objects.get(pk=booking_id, visitor=self.request.user)
                if b.payment_status == 'paid':
                    return None
                return b.total_fare
        except Exception:
            return None

    def _mark_booking_paid(self, payment):
        try:
            if payment.payment_type == 'booking':
                from apps.bookings.models import Booking
                Booking.objects.filter(pk=payment.booking_id).update(
                    payment_status='paid', status='confirmed'
                )
            else:
                from apps.cabs.models import CabBooking
                CabBooking.objects.filter(pk=payment.booking_id).update(
                    payment_status='paid', status='confirmed'
                )
        except Exception as e:
            logger.error("Failed to mark booking paid: %s", e)
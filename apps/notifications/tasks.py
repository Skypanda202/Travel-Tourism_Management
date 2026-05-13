"""
Smart Tourism — Notification Tasks
Called by Django signals after booking/payment events.
"""
import logging
from celery import shared_task

logger = logging.getLogger(__name__)


def _create_notification(user_id, notif_type, title, message, data=None):
    from apps.notifications.models import Notification
    Notification.objects.create(
        user_id=user_id,
        type=notif_type,
        title=title,
        message=message,
        data=data or {},
    )


@shared_task(ignore_result=True)
def notify_booking_confirmed(booking_id):
    from apps.bookings.models import Booking
    try:
        b = Booking.objects.select_related('visitor', 'place').get(pk=booking_id)
        _create_notification(
            b.visitor_id, 'booking_confirmed',
            'Booking Confirmed! 🎉',
            f"Your booking for {b.place.name} on {b.visit_date} (Ref: {b.booking_ref}) is confirmed.",
            data={'booking_id': booking_id, 'booking_ref': b.booking_ref},
        )
    except Exception as e:
        logger.error("notify_booking_confirmed failed: %s", e)


@shared_task(ignore_result=True)
def notify_booking_cancelled(booking_id):
    from apps.bookings.models import Booking
    try:
        b = Booking.objects.select_related('visitor', 'place').get(pk=booking_id)
        _create_notification(
            b.visitor_id, 'booking_cancelled',
            'Booking Cancelled',
            f"Your booking {b.booking_ref} for {b.place.name} has been cancelled.",
            data={'booking_id': booking_id},
        )
    except Exception as e:
        logger.error("notify_booking_cancelled failed: %s", e)


@shared_task(ignore_result=True)
def notify_payment_success(payment_id):
    from apps.payments.models import Payment
    try:
        p = Payment.objects.select_related('user').get(pk=payment_id)
        _create_notification(
            p.user_id, 'payment_success',
            'Payment Successful ✅',
            f"Payment of ₹{p.net_amount} (Ref: {p.transaction_ref}) was successful.",
            data={'payment_id': payment_id, 'transaction_ref': p.transaction_ref},
        )
    except Exception as e:
        logger.error("notify_payment_success failed: %s", e)


@shared_task(ignore_result=True)
def notify_cab_confirmed(cab_booking_id):
    from apps.cabs.models import CabBooking
    try:
        b = CabBooking.objects.select_related('visitor', 'cab_type').get(pk=cab_booking_id)
        _create_notification(
            b.visitor_id, 'cab_confirmed',
            'Cab Booking Confirmed 🚗',
            f"Your {b.cab_type.name} from {b.pickup_address} on "
            f"{b.pickup_datetime.strftime('%d %b %Y %H:%M')} is confirmed. "
            f"Driver: {b.driver_name or 'TBA'}",
            data={'cab_booking_id': cab_booking_id, 'booking_ref': b.booking_ref},
        )
    except Exception as e:
        logger.error("notify_cab_confirmed failed: %s", e)
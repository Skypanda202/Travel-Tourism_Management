"""
Smart Tourism — Booking Signals
Fires Celery notification tasks when booking status changes.
"""
from django.db.models.signals import post_save
from django.dispatch import receiver
import logging
from apps.bookings.models import Booking

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Booking)
def booking_status_changed(sender, instance, created, **kwargs):
    from apps.notifications.tasks import notify_booking_confirmed, notify_booking_cancelled

    if created:
        return   # New bookings are pending — no notification yet

    try:
        if instance.status == 'confirmed':
            notify_booking_confirmed.delay(instance.pk)
        elif instance.status == 'cancelled':
            notify_booking_cancelled.delay(instance.pk)
    except Exception as exc:
        logger.warning("Could not enqueue booking notification for %s: %s", instance.pk, exc)

"""
Smart Tourism — Booking Signals
Fires Celery notification tasks when booking status changes.
"""
from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.bookings.models import Booking


@receiver(post_save, sender=Booking)
def booking_status_changed(sender, instance, created, **kwargs):
    from apps.notifications.tasks import notify_booking_confirmed, notify_booking_cancelled

    if created:
        return   # New bookings are pending — no notification yet

    if instance.status == 'confirmed':
        notify_booking_confirmed.delay(instance.pk)
    elif instance.status == 'cancelled':
        notify_booking_cancelled.delay(instance.pk)
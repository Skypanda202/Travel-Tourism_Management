"""Smart Tourism — Payment Signals."""
from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.payments.models import Payment


@receiver(post_save, sender=Payment)
def payment_status_changed(sender, instance, created, **kwargs):
    from apps.notifications.tasks import notify_payment_success
    if not created and instance.status == 'success':
        notify_payment_success.delay(instance.pk)
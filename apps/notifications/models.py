"""Smart Tourism — Notifications Models."""
from django.db import models


class Notification(models.Model):
    """In-app notification for a user."""

    TYPE_CHOICES = [
        ('booking_confirmed',  'Booking Confirmed'),
        ('booking_cancelled',  'Booking Cancelled'),
        ('booking_completed',  'Booking Completed'),
        ('payment_success',    'Payment Successful'),
        ('payment_failed',     'Payment Failed'),
        ('review_approved',    'Review Approved'),
        ('review_rejected',    'Review Rejected'),
        ('cab_confirmed',      'Cab Booking Confirmed'),
        ('cab_cancelled',      'Cab Booking Cancelled'),
        ('system',             'System Notification'),
        ('promo',              'Promotion'),
    ]

    user       = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='notifications')
    type       = models.CharField(max_length=25, choices=TYPE_CHOICES)
    title      = models.CharField(max_length=255)
    message    = models.TextField()
    is_read    = models.BooleanField(default=False)
    data       = models.JSONField(null=True, blank=True)   # optional metadata (booking_id, etc.)
    created_at = models.DateTimeField(auto_now_add=True)
    read_at    = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'notifications'
        ordering = ['-created_at']
        indexes  = [
            models.Index(fields=['user', 'is_read']),
        ]

    def __str__(self):
        return f"[{self.type}] {self.user.email}: {self.title}"

    def mark_read(self):
        from django.utils import timezone
        if not self.is_read:
            self.is_read = True
            self.read_at = timezone.now()
            self.save(update_fields=['is_read', 'read_at'])
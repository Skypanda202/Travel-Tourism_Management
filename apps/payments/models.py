"""Smart Tourism — Payments Models."""
from django.db import models
import uuid


class Payment(models.Model):
    """Payment record for a booking or cab booking."""

    TYPE_CHOICES = [
        ('booking',     'Tour Booking'),
        ('cab_booking', 'Cab Booking'),
    ]

    STATUS_CHOICES = [
        ('initiated',  'Initiated'),
        ('pending',    'Pending'),
        ('success',    'Success'),
        ('failed',     'Failed'),
        ('refunded',   'Refunded'),
        ('cancelled',  'Cancelled'),
    ]

    METHOD_CHOICES = [
        ('card',   'Credit/Debit Card'),
        ('upi',    'UPI'),
        ('netbanking', 'Net Banking'),
        ('wallet', 'Wallet'),
        ('cash',   'Cash'),
        ('free',   'Free Entry'),
    ]

    # Unique transaction reference
    transaction_ref = models.CharField(max_length=40, unique=True, blank=True)

    # Who paid
    user = models.ForeignKey('users.User', on_delete=models.PROTECT, related_name='payments')

    # What was paid for (generic FK pattern)
    payment_type    = models.CharField(max_length=15, choices=TYPE_CHOICES)
    booking_id      = models.PositiveIntegerField(null=True, blank=True)   # FK to Booking or CabBooking

    # Amount
    amount   = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='INR')
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    net_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    # Gateway
    payment_method   = models.CharField(max_length=15, choices=METHOD_CHOICES, default='card')
    gateway          = models.CharField(max_length=50, blank=True, help_text="Razorpay, Stripe, etc.")
    gateway_order_id = models.CharField(max_length=100, blank=True)
    gateway_payment_id = models.CharField(max_length=100, blank=True)
    gateway_signature  = models.CharField(max_length=255, blank=True)

    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default='initiated')

    # Timestamps
    initiated_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    refunded_at  = models.DateTimeField(null=True, blank=True)
    failure_reason = models.TextField(blank=True)

    class Meta:
        db_table = 'payments'
        ordering = ['-initiated_at']
        indexes  = [
            models.Index(fields=['user', 'status']),
            models.Index(fields=['transaction_ref']),
        ]

    def save(self, *args, **kwargs):
        if not self.transaction_ref:
            self.transaction_ref = f"TXN{uuid.uuid4().hex[:16].upper()}"
        if not self.net_amount:
            self.net_amount = self.amount - self.discount
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.transaction_ref} — ₹{self.amount} ({self.status})"
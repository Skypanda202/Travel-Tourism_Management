"""
Smart Tourism — Bookings Models
Tour bookings made by visitors.
"""
from django.db import models
from django.core.validators import MinValueValidator
import uuid


class Booking(models.Model):
    """Tour booking by a visitor for a tourist place."""

    STATUS_CHOICES = [
        ('pending',   'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
        ('refunded',  'Refunded'),
    ]

    PAYMENT_STATUS_CHOICES = [
        ('unpaid',   'Unpaid'),
        ('paid',     'Paid'),
        ('refunded', 'Refunded'),
        ('failed',   'Failed'),
    ]

    # Unique booking reference
    booking_ref = models.CharField(max_length=20, unique=True, blank=True)

    # Relations
    visitor     = models.ForeignKey('users.User',           on_delete=models.PROTECT, related_name='bookings')
    place       = models.ForeignKey('places.TouristPlace',  on_delete=models.PROTECT, related_name='bookings')

    # Visit details
    visit_date    = models.DateField()
    num_adults    = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    num_children  = models.PositiveIntegerField(default=0)
    special_notes = models.TextField(blank=True)

    # Pricing
    adult_fee    = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    children_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    currency     = models.CharField(max_length=3, default='INR')
    discount     = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    # Status
    status         = models.CharField(max_length=10, choices=STATUS_CHOICES,         default='pending')
    payment_status = models.CharField(max_length=10, choices=PAYMENT_STATUS_CHOICES, default='unpaid')

    # Timestamps
    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)
    cancelled_at = models.DateTimeField(null=True, blank=True)
    cancel_reason = models.TextField(blank=True)

    class Meta:
        db_table = 'bookings'
        ordering = ['-created_at']
        indexes  = [
            models.Index(fields=['visitor', 'status']),
            models.Index(fields=['place', 'visit_date']),
            models.Index(fields=['booking_ref']),
        ]

    def save(self, *args, **kwargs):
        if not self.booking_ref:
            self.booking_ref = f"BK{uuid.uuid4().hex[:10].upper()}"
        # Auto-calculate total
        if not self.total_amount:
            self.total_amount = (
                (self.adult_fee * self.num_adults) +
                (self.children_fee * self.num_children) -
                self.discount
            )
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.booking_ref} — {self.visitor.email} @ {self.place.name}"

    @property
    def total_visitors(self):
        return self.num_adults + self.num_children
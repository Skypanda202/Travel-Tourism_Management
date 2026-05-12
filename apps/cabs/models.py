"""Smart Tourism — Cab Booking Models."""
from django.db import models
from django.core.validators import MinValueValidator
import uuid


class CabType(models.Model):
    """Type of cab (Hatchback, SUV, Tempo Traveller, etc.)."""
    name             = models.CharField(max_length=100, unique=True)
    description      = models.TextField(blank=True)
    capacity         = models.PositiveIntegerField(default=4)
    price_per_km     = models.DecimalField(max_digits=6, decimal_places=2)
    base_fare        = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    image            = models.ImageField(upload_to='cabs/', null=True, blank=True)
    is_ac            = models.BooleanField(default=True)
    is_available     = models.BooleanField(default=True)
    created_at       = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'cab_types'

    def __str__(self):
        return f"{self.name} (₹{self.price_per_km}/km)"


class CabBooking(models.Model):
    """A visitor booking a cab."""

    STATUS_CHOICES = [
        ('pending',   'Pending'),
        ('confirmed', 'Confirmed'),
        ('on_trip',   'On Trip'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    PAYMENT_STATUS_CHOICES = [
        ('unpaid',   'Unpaid'),
        ('paid',     'Paid'),
        ('refunded', 'Refunded'),
    ]

    booking_ref     = models.CharField(max_length=20, unique=True, blank=True)
    visitor         = models.ForeignKey('users.User', on_delete=models.PROTECT, related_name='cab_bookings')
    cab_type        = models.ForeignKey(CabType, on_delete=models.PROTECT, related_name='bookings')

    # Route
    pickup_address      = models.TextField()
    pickup_latitude     = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    pickup_longitude    = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    dropoff_address     = models.TextField()
    dropoff_latitude    = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    dropoff_longitude   = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    distance_km         = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)

    # Schedule
    pickup_datetime  = models.DateTimeField()
    num_passengers   = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    special_requests = models.TextField(blank=True)

    # Pricing
    base_fare    = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    distance_fare = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_fare   = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    currency     = models.CharField(max_length=3, default='INR')

    # Driver (if assigned)
    driver_name   = models.CharField(max_length=200, blank=True)
    driver_phone  = models.CharField(max_length=20, blank=True)
    vehicle_number = models.CharField(max_length=20, blank=True)

    status         = models.CharField(max_length=10, choices=STATUS_CHOICES,         default='pending')
    payment_status = models.CharField(max_length=10, choices=PAYMENT_STATUS_CHOICES, default='unpaid')

    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'cab_bookings'
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.booking_ref:
            self.booking_ref = f"CB{uuid.uuid4().hex[:10].upper()}"
        # Auto calculate fare
        if self.distance_km and not self.total_fare:
            self.distance_fare = self.cab_type.price_per_km * self.distance_km
            self.total_fare    = self.cab_type.base_fare + self.distance_fare
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.booking_ref} — {self.visitor.email}"
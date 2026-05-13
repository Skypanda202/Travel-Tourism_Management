"""
Smart Tourism — Analytics Models
Tracks visitor activity and aggregated daily/monthly/yearly stats.
"""
from django.db import models


class VisitorActivity(models.Model):
    """
    Raw event log — every meaningful user action.
    Consumed by the analytics aggregation tasks.
    """
    ACTION_CHOICES = [
        ('view_place',      'View Place'),
        ('search',          'Search'),
        ('create_booking',  'Create Booking'),
        ('cancel_booking',  'Cancel Booking'),
        ('write_review',    'Write Review'),
        ('add_favorite',    'Add Favorite'),
        ('remove_favorite', 'Remove Favorite'),
        ('create_plan',     'Create Travel Plan'),
        ('book_cab',        'Book Cab'),
        ('view_page',       'View Page'),
        ('login',           'Login'),
        ('register',        'Register'),
    ]

    user          = models.ForeignKey(
        'users.User', on_delete=models.SET_NULL, null=True, blank=True,
        related_name='activities'
    )
    action        = models.CharField(max_length=20, choices=ACTION_CHOICES)
    resource_type = models.CharField(max_length=50, blank=True)   # e.g. "TouristPlace"
    resource_id   = models.PositiveIntegerField(null=True, blank=True)
    resource_name = models.CharField(max_length=255, blank=True)

    # Request metadata
    ip_address    = models.GenericIPAddressField(null=True, blank=True)
    user_agent    = models.TextField(blank=True)
    session_key   = models.CharField(max_length=40, blank=True)
    referrer      = models.URLField(blank=True)

    # Extra payload (JSON-like flat storage)
    extra_data    = models.JSONField(null=True, blank=True)

    created_at    = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        db_table = 'visitor_activities'
        ordering = ['-created_at']
        indexes  = [
            models.Index(fields=['user', 'action']),
            models.Index(fields=['action', 'created_at']),
            models.Index(fields=['resource_type', 'resource_id']),
        ]

    def __str__(self):
        who = self.user.email if self.user else 'anonymous'
        return f"{who} → {self.action} ({self.created_at:%Y-%m-%d %H:%M})"


class DailyAnalytics(models.Model):
    """
    Pre-aggregated platform-wide daily snapshot.
    Populated nightly by a Celery beat task.
    """
    date               = models.DateField(unique=True)

    # Traffic
    total_visits       = models.PositiveIntegerField(default=0)
    unique_visitors    = models.PositiveIntegerField(default=0)
    new_registrations  = models.PositiveIntegerField(default=0)

    # Bookings
    total_bookings     = models.PositiveIntegerField(default=0)
    confirmed_bookings = models.PositiveIntegerField(default=0)
    cancelled_bookings = models.PositiveIntegerField(default=0)
    completed_bookings = models.PositiveIntegerField(default=0)

    # Cabs
    cab_bookings       = models.PositiveIntegerField(default=0)

    # Revenue
    booking_revenue    = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    cab_revenue        = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    total_revenue      = models.DecimalField(max_digits=14, decimal_places=2, default=0)

    # Reviews
    total_reviews      = models.PositiveIntegerField(default=0)

    # Search / favorites
    total_searches     = models.PositiveIntegerField(default=0)
    total_favorites    = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'daily_analytics'
        ordering = ['-date']

    def __str__(self):
        return f"Analytics: {self.date} — Revenue ₹{self.total_revenue}"


class PlaceAnalytics(models.Model):
    """Per-place daily stats."""
    place      = models.ForeignKey('places.TouristPlace', on_delete=models.CASCADE,
                                related_name='analytics')
    date       = models.DateField()
    views      = models.PositiveIntegerField(default=0)
    bookings   = models.PositiveIntegerField(default=0)
    favorites  = models.PositiveIntegerField(default=0)
    reviews    = models.PositiveIntegerField(default=0)
    revenue    = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    class Meta:
        db_table        = 'place_analytics'
        unique_together = ('place', 'date')
        ordering        = ['-date']

    def __str__(self):
        return f"{self.place.name} — {self.date}"
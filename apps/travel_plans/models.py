"""Smart Tourism — Travel Plans Models."""
from django.db import models


class TravelPlan(models.Model):
    """A visitor's personal travel itinerary."""

    VISIBILITY_CHOICES = [
        ('private', 'Private'),
        ('public',  'Public'),
        ('shared',  'Shared via Link'),
    ]

    visitor    = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='travel_plans')
    title      = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    start_date = models.DateField()
    end_date   = models.DateField()
    budget     = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    currency   = models.CharField(max_length=3, default='INR')
    visibility = models.CharField(max_length=10, choices=VISIBILITY_CHOICES, default='private')
    share_token = models.CharField(max_length=50, blank=True, unique=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'travel_plans'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} ({self.visitor.email})"

    def save(self, *args, **kwargs):
        if self.visibility == 'shared' and not self.share_token:
            import uuid
            self.share_token = uuid.uuid4().hex
        super().save(*args, **kwargs)

    @property
    def duration_days(self):
        return (self.end_date - self.start_date).days + 1


class TravelPlanItem(models.Model):
    """A single stop/activity in a travel plan."""
    plan     = models.ForeignKey(TravelPlan, on_delete=models.CASCADE, related_name='items')
    place    = models.ForeignKey('places.TouristPlace', on_delete=models.CASCADE, related_name='plan_items')
    day      = models.PositiveIntegerField(default=1)
    order    = models.PositiveIntegerField(default=0)
    visit_time  = models.TimeField(null=True, blank=True)
    duration_hours = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)
    notes    = models.TextField(blank=True)
    transport_to = models.CharField(max_length=100, blank=True, help_text="How to reach from previous stop")
    estimated_cost = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    class Meta:
        db_table = 'travel_plan_items'
        ordering = ['day', 'order']

    def __str__(self):
        return f"Day {self.day}: {self.place.name}"
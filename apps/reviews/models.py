"""Smart Tourism — Reviews & Ratings Models."""
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Review(models.Model):
    """Visitor review and rating for a tourist place."""

    STATUS_CHOICES = [
        ('pending',  'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    user    = models.ForeignKey('users.User',          on_delete=models.CASCADE, related_name='reviews')
    place   = models.ForeignKey('places.TouristPlace', on_delete=models.CASCADE, related_name='reviews')
    booking = models.ForeignKey('bookings.Booking', on_delete=models.SET_NULL,
                                null=True, blank=True, related_name='review')

    # Content
    rating  = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    title   = models.CharField(max_length=255, blank=True)
    content = models.TextField()

    # Sub-ratings
    cleanliness_rating   = models.PositiveSmallIntegerField(null=True, blank=True,
                            validators=[MinValueValidator(1), MaxValueValidator(5)])
    accessibility_rating = models.PositiveSmallIntegerField(null=True, blank=True,
                            validators=[MinValueValidator(1), MaxValueValidator(5)])
    value_rating         = models.PositiveSmallIntegerField(null=True, blank=True,
                            validators=[MinValueValidator(1), MaxValueValidator(5)])

    # Moderation
    status      = models.CharField(max_length=10, choices=STATUS_CHOICES, default='approved')
    is_verified = models.BooleanField(default=False)   # tied to a booking
    helpful_count = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table        = 'reviews'
        unique_together = ('user', 'place')   # one review per place per user
        ordering        = ['-created_at']

    def __str__(self):
        return f"{self.user.email} → {self.place.name} ({self.rating}★)"

    def save(self, *args, **kwargs):
        # Mark as verified if tied to a completed booking
        if self.booking and self.booking.status == 'completed':
            self.is_verified = True
        super().save(*args, **kwargs)
        # Update place avg_rating & total_reviews
        self._update_place_rating()

    def _update_place_rating(self):
        from django.db.models import Avg
        from apps.places.models import TouristPlace
        stats = Review.objects.filter(place=self.place, status='approved').aggregate(
            avg=Avg('rating'), count=models.Count('id')
        )
        TouristPlace.objects.filter(pk=self.place_id).update(
            avg_rating=round(stats['avg'] or 0, 2),
            total_reviews=stats['count'],
        )


class ReviewImage(models.Model):
    """Images attached to a review."""
    review     = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='images')
    image      = models.ImageField(upload_to='reviews/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'review_images'

    def __str__(self):
        return f"Image for review #{self.review_id}"
"""
Smart Tourism — Places Models
TouristPlace, Category, PlaceImage, Favorite
"""
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.text import slugify


class Category(models.Model):
    """Place category: Beach, Mountain, Museum, etc."""
    name        = models.CharField(max_length=100, unique=True)
    slug        = models.SlugField(max_length=120, unique=True, blank=True)
    description = models.TextField(blank=True)
    icon        = models.CharField(max_length=50, blank=True, help_text="Icon class or emoji")
    image       = models.ImageField(upload_to='categories/', null=True, blank=True)
    is_active   = models.BooleanField(default=True)
    sort_order  = models.PositiveIntegerField(default=0)
    created_at  = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table  = 'categories'
        ordering  = ['sort_order', 'name']
        verbose_name_plural = 'Categories'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class TouristPlace(models.Model):
    """Core tourist place record."""

    STATUS_CHOICES = [
        ('draft',     'Draft'),
        ('published', 'Published'),
        ('archived',  'Archived'),
    ]

    # Basic
    name        = models.CharField(max_length=255)
    slug        = models.SlugField(max_length=280, unique=True, blank=True)
    description = models.TextField()
    short_desc  = models.CharField(max_length=500, blank=True)
    category    = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='places')
    tags        = models.CharField(max_length=500, blank=True, help_text="Comma-separated tags")
    status      = models.CharField(max_length=10, choices=STATUS_CHOICES, default='published')

    # Location
    address    = models.TextField()
    city       = models.CharField(max_length=100)
    state      = models.CharField(max_length=100, blank=True)
    country    = models.CharField(max_length=100)
    zip_code   = models.CharField(max_length=20, blank=True)
    latitude   = models.DecimalField(max_digits=9, decimal_places=6)
    longitude  = models.DecimalField(max_digits=9, decimal_places=6)
    google_maps_url = models.URLField(blank=True)

    # Media
    cover_image = models.ImageField(upload_to='places/', null=True, blank=True)

    # Pricing
    entry_fee         = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    entry_fee_currency = models.CharField(max_length=3, default='INR')
    is_free           = models.BooleanField(default=False)

    # Operational
    opening_time    = models.TimeField(null=True, blank=True)
    closing_time    = models.TimeField(null=True, blank=True)
    open_days       = models.CharField(max_length=200, blank=True, help_text="e.g. Mon-Fri, Sun")
    best_time_to_visit = models.CharField(max_length=200, blank=True)

    # Stats (denormalised)
    avg_rating    = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    total_reviews = models.PositiveIntegerField(default=0)
    total_visits  = models.PositiveIntegerField(default=0)
    total_bookings = models.PositiveIntegerField(default=0)

    # Meta
    created_by = models.ForeignKey(
        'users.User', on_delete=models.SET_NULL, null=True, related_name='created_places'
    )
    is_featured    = models.BooleanField(default=False)
    is_recommended = models.BooleanField(default=False)
    created_at     = models.DateTimeField(auto_now_add=True)
    updated_at     = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'tourist_places'
        ordering = ['-is_featured', '-avg_rating', 'name']
        indexes  = [
            models.Index(fields=['city', 'country']),
            models.Index(fields=['category']),
            models.Index(fields=['status']),
            models.Index(fields=['latitude', 'longitude']),
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug, n   = base_slug, 1
            while TouristPlace.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{n}"
                n   += 1
            self.slug = slug
        if self.entry_fee == 0:
            self.is_free = True
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.city})"

    @property
    def tag_list(self):
        return [t.strip() for t in self.tags.split(',') if t.strip()]


class PlaceImage(models.Model):
    """Additional images for a tourist place."""
    place    = models.ForeignKey(TouristPlace, on_delete=models.CASCADE, related_name='images')
    image    = models.ImageField(upload_to='places/gallery/')
    caption  = models.CharField(max_length=255, blank=True)
    is_cover = models.BooleanField(default=False)
    sort_order = models.PositiveIntegerField(default=0)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'place_images'
        ordering = ['sort_order', 'uploaded_at']

    def __str__(self):
        return f"Image for {self.place.name}"


class Favorite(models.Model):
    """Visitor's saved / favourite places."""
    user       = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='favorites')
    place      = models.ForeignKey(TouristPlace, on_delete=models.CASCADE, related_name='favorited_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table        = 'favorites'
        unique_together = ('user', 'place')
        ordering        = ['-created_at']

    def __str__(self):
        return f"{self.user.email} ❤ {self.place.name}"
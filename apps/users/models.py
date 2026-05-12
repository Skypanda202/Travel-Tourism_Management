"""
Smart Tourism — User Models
Custom AbstractUser with role-based access.
"""
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator


class User(AbstractUser):
    """
    Extended user model.
    Roles:
      - admin   : platform administrator
      - visitor : tourist / end-user
    """

    ROLE_CHOICES = [
        ('admin',   'Admin'),
        ('visitor', 'Visitor'),
    ]

    # Override email → required + unique
    email = models.EmailField(unique=True)

    # Role
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='visitor')

    # Profile
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits."
    )
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    avatar       = models.ImageField(upload_to='avatars/', null=True, blank=True)
    bio          = models.TextField(blank=True)
    date_of_birth = models.DateField(null=True, blank=True)

    # Location
    city    = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    latitude  = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    # Status
    is_verified       = models.BooleanField(default=False)
    is_active         = models.BooleanField(default=True)
    email_verified_at = models.DateTimeField(null=True, blank=True)

    # Preferences
    preferred_language = models.CharField(max_length=10, default='en')
    newsletter_opt_in  = models.BooleanField(default=False)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        db_table = 'users'
        ordering = ['-created_at']
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return f"{self.get_full_name()} <{self.email}>"

    # ── helpers ────────────────────────────────────────────────────────────────
    @property
    def is_admin(self):
        return self.role == 'admin' or self.is_staff

    @property
    def is_visitor(self):
        return self.role == 'visitor'

    @property
    def full_name(self):
        return self.get_full_name() or self.username

    def get_avatar_url(self):
        if self.avatar:
            return self.avatar.url
        return None


class VisitorProfile(models.Model):
    """
    Extended profile for visitors — preferences & stats.
    Created automatically when a visitor registers.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='visitor_profile')

    # Travel preferences
    TRAVEL_STYLE_CHOICES = [
        ('adventure', 'Adventure'),
        ('leisure',   'Leisure'),
        ('cultural',  'Cultural'),
        ('business',  'Business'),
        ('family',    'Family'),
    ]
    travel_style        = models.CharField(max_length=20, choices=TRAVEL_STYLE_CHOICES, blank=True)
    preferred_categories = models.ManyToManyField('places.Category', blank=True)

    # Stats (denormalised for speed)
    total_bookings    = models.PositiveIntegerField(default=0)
    total_reviews     = models.PositiveIntegerField(default=0)
    total_places_visited = models.PositiveIntegerField(default=0)

    # Social
    instagram_handle = models.CharField(max_length=100, blank=True)
    twitter_handle   = models.CharField(max_length=100, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'visitor_profiles'

    def __str__(self):
        return f"Profile: {self.user.email}"
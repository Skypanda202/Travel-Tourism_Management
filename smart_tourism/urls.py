"""
Smart Tourism Management System — Root URL Configuration
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenRefreshView
from apps.users.views.auth_views import (
    GoogleLoginView,
    LoginView,
    ResendVerificationEmailView,
    VerifyEmailView,
)
from .views import register
urlpatterns = [

    # Admin Panel
    path('admin/', admin.site.urls),

    # App URLs
    path('users/', include('apps.users.urls')),
    path('places/', include('apps.places.urls')),
    path('bookings/', include('apps.bookings.urls')),
    path('cabs/', include('apps.cabs.urls')),
    path('reviews/', include('apps.reviews.urls')),
    path('travel-plans/', include('apps.travel_plans.urls')),
    path('payments/', include('apps.payments.urls')),
    path('analytics/', include('apps.analytics.urls')),
    path('notifications/', include('apps.notifications.urls')),

    # API aliases used by the React frontend.
    path('api/users/', include('apps.users.urls')),
    path('api/places/', include('apps.places.urls')),
    path('api/bookings/', include('apps.bookings.urls')),
    path('api/cabs/', include('apps.cabs.urls')),
    path('api/reviews/', include('apps.reviews.urls')),
    path('api/travel-plans/', include('apps.travel_plans.urls')),
    path('api/payments/', include('apps.payments.urls')),
    path('api/analytics/', include('apps.analytics.urls')),
    path('api/notifications/', include('apps.notifications.urls')),
    path('api/ai/', include('ai_assistant.urls')),
    path('api/v1/auth/', include('apps.users.views.auth_urls')),
    path('api/v1/users/', include('apps.users.urls')),
    path('api/v1/places/', include('apps.places.urls')),
    path('api/v1/bookings/', include('apps.bookings.urls')),
    path('api/v1/cabs/', include('apps.cabs.urls')),
    path('api/v1/reviews/', include('apps.reviews.urls')),
    path('api/v1/travel-plans/', include('apps.travel_plans.urls')),
    path('api/v1/payments/', include('apps.payments.urls')),
    path('api/v1/analytics/', include('apps.analytics.urls')),
    path('api/v1/notifications/', include('apps.notifications.urls')),
    path('api/v1/ai/', include('ai_assistant.urls')),
    path(
        "api/login/",
        LoginView.as_view(),
    ),
    path("api/google/", GoogleLoginView.as_view()),
    path("api/verify-email/", VerifyEmailView.as_view()),
    path("api/resend-verification/", ResendVerificationEmailView.as_view()),

    path(
        "api/token/refresh/",
        TokenRefreshView.as_view(),
    ),
    path("api/register/", register),
]

# Media + Static Files
if settings.DEBUG:

    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )

    urlpatterns += static(
        settings.STATIC_URL,
        document_root=settings.STATIC_ROOT
    )

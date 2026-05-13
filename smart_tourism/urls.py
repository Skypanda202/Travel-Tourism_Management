"""
Smart Tourism Management System — Root URL Configuration
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (TokenObtainPairView,
    TokenRefreshView,
)
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
    path('api/ai/', include('ai_assistant.urls')),
    path(
        "api/login/",
        TokenObtainPairView.as_view(),
    ),

    path(
        "api/token/refresh/",
        TokenRefreshView.as_view(),
    ),
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
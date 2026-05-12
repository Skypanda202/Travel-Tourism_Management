"""
Smart Tourism Management System — Root URL Configuration
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    # Admin Panel
    path('admin/', admin.site.urls),

    # App URLs
    path('users/', include('users.urls')),
    path('places/', include('places.urls')),
    path('bookings/', include('bookings.urls')),
    path('cabs/', include('cabs.urls')),
    path('reviews/', include('reviews.urls')),
    path('travel-plans/', include('travel_plans.urls')),
    path('payments/', include('payments.urls')),
    path('analytics/', include('analytics.urls')),
    path('notifications/', include('notifications.urls')),
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
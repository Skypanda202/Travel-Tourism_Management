"""
Smart Tourism Management System — Root URL Configuration
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenRefreshView
from apps.users.views.auth_views import LoginView
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
    path(
        "api/login/",
        LoginView.as_view(),
    ),

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

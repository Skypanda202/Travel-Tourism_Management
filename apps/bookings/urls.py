from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.bookings.views import BookingViewSet

router = DefaultRouter()
router.register(r'', BookingViewSet, basename='bookings')

urlpatterns = [path('', include(router.urls))]
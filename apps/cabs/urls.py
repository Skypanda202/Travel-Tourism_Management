from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.cabs.views import CabTypeViewSet, CabBookingViewSet

router = DefaultRouter()
router.register(r'types',    CabTypeViewSet,    basename='cab-types')
router.register(r'bookings', CabBookingViewSet, basename='cab-bookings')

urlpatterns = [path('', include(router.urls))]
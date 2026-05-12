"""Places URL configuration."""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.places.views import CategoryViewSet, TouristPlaceViewSet

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='categories')
router.register(r'',           TouristPlaceViewSet, basename='places')

urlpatterns = [
    path('', include(router.urls)),
]
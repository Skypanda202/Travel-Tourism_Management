from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.travel_plans.views import TravelPlanViewSet

router = DefaultRouter()
router.register(r'', TravelPlanViewSet, basename='travel-plans')
urlpatterns = [path('', include(router.urls))]
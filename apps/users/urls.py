"""User management URL routes."""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.users.views.user_views import UserViewSet, VisitorProfileViewSet

router = DefaultRouter()
router.register(r'', UserViewSet, basename='users')

# Non-router profile endpoints
from apps.users.views.user_views import VisitorProfileViewSet
profile_vp = VisitorProfileViewSet.as_view({'get': 'profile', 'patch': 'profile'})
visitor_profile_vp = VisitorProfileViewSet.as_view({'get': 'visitor_profile', 'patch': 'visitor_profile'})
favorites_vp = VisitorProfileViewSet.as_view({'get': 'favorites'})
dashboard_vp = VisitorProfileViewSet.as_view({'get': 'dashboard'})
delete_account_vp = VisitorProfileViewSet.as_view({'delete': 'delete_account'})

urlpatterns = [
    path('profile/',         profile_vp,         name='user-profile'),
    path('visitor-profile/', visitor_profile_vp, name='visitor-profile'),
    path('favorites/',       favorites_vp,       name='user-favorites'),
    path('dashboard/',       dashboard_vp,       name='user-dashboard'),
    path('delete-account/',  delete_account_vp,  name='delete-account'),
    path('',                 include(router.urls)),
]

"""Auth URL routes."""
from django.urls import path
from apps.users.views.auth_views import (
    LoginView,
    RegisterView,
    LogoutView,
    TokenRefreshCustomView,
    ChangePasswordView,
    me,
)

urlpatterns = [
    path('login/',           LoginView.as_view(),              name='auth-login'),
    path('register/',        RegisterView.as_view(),           name='auth-register'),
    path('logout/',          LogoutView.as_view(),             name='auth-logout'),
    path('token/refresh/',   TokenRefreshCustomView.as_view(), name='auth-token-refresh'),
    path('change-password/', ChangePasswordView.as_view(),     name='auth-change-password'),
    path('me/',              me,                               name='auth-me'),
]
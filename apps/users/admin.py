"""Smart Tourism — Users Admin Registration."""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from apps.users.models import User, VisitorProfile


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display  = ['email', 'username', 'full_name', 'role', 'is_active', 'is_verified', 'created_at']
    list_filter   = ['role', 'is_active', 'is_staff', 'is_verified']
    search_fields = ['email', 'username', 'first_name', 'last_name']
    ordering      = ['-created_at']

    fieldsets = (
        (None,            {'fields': ('email', 'username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'phone_number', 'avatar', 'bio', 'date_of_birth')}),
        ('Location',      {'fields': ('city', 'country', 'latitude', 'longitude')}),
        ('Permissions',   {'fields': ('role', 'is_active', 'is_staff', 'is_superuser', 'is_verified', 'groups', 'user_permissions')}),
        ('Preferences',   {'fields': ('preferred_language', 'newsletter_opt_in')}),
        ('Timestamps',    {'fields': ('date_joined', 'last_login'), 'classes': ('collapse',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields':  ('email', 'username', 'first_name', 'last_name', 'role', 'password1', 'password2'),
        }),
    )
    readonly_fields = ['date_joined', 'last_login', 'created_at', 'updated_at']


@admin.register(VisitorProfile)
class VisitorProfileAdmin(admin.ModelAdmin):
    list_display  = ['user', 'travel_style', 'total_bookings', 'total_reviews']
    search_fields = ['user__email', 'user__username']
    raw_id_fields = ['user']
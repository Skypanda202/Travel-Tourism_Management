"""Smart Tourism — Places Admin."""
from django.contrib import admin
from apps.places.models import Category, TouristPlace, PlaceImage, Favorite


class PlaceImageInline(admin.TabularInline):
    model  = PlaceImage
    extra  = 1
    fields = ['image', 'caption', 'is_cover', 'sort_order']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display  = ['name', 'slug', 'is_active', 'sort_order']
    prepopulated_fields = {'slug': ('name',)}
    list_filter   = ['is_active']


@admin.register(TouristPlace)
class TouristPlaceAdmin(admin.ModelAdmin):
    list_display   = ['name', 'city', 'country', 'category', 'status', 'avg_rating', 'is_featured', 'created_at']
    list_filter    = ['status', 'is_featured', 'is_free', 'category', 'country']
    search_fields  = ['name', 'city', 'country', 'description']
    prepopulated_fields = {'slug': ('name',)}
    inlines        = [PlaceImageInline]
    readonly_fields = ['avg_rating', 'total_reviews', 'total_visits', 'total_bookings', 'created_at', 'updated_at']
    raw_id_fields  = ['created_by', 'category']
    fieldsets = (
        ('Basic',     {'fields': ('name', 'slug', 'description', 'short_desc', 'category', 'tags', 'status')}),
        ('Location',  {'fields': ('address', 'city', 'state', 'country', 'zip_code', 'latitude', 'longitude', 'google_maps_url')}),
        ('Media',     {'fields': ('cover_image',)}),
        ('Pricing',   {'fields': ('entry_fee', 'entry_fee_currency', 'is_free')}),
        ('Hours',     {'fields': ('opening_time', 'closing_time', 'open_days', 'best_time_to_visit')}),
        ('Stats',     {'fields': ('avg_rating', 'total_reviews', 'total_visits', 'total_bookings'), 'classes': ('collapse',)}),
        ('Flags',     {'fields': ('is_featured', 'is_recommended', 'created_by')}),
    )


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ['user', 'place', 'created_at']
    raw_id_fields = ['user', 'place']
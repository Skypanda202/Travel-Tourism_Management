from django.contrib import admin
from apps.reviews.models import Review, ReviewImage


class ReviewImageInline(admin.TabularInline):
    model = ReviewImage
    extra = 0


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display  = ['user', 'place', 'rating', 'status', 'is_verified', 'helpful_count', 'created_at']
    list_filter   = ['status', 'rating', 'is_verified']
    search_fields = ['user__email', 'place__name', 'content']
    raw_id_fields = ['user', 'place', 'booking']
    inlines       = [ReviewImageInline]
    actions       = ['approve_reviews', 'reject_reviews']

    def approve_reviews(self, request, queryset):
        queryset.update(status='approved')
    approve_reviews.short_description = "Approve selected reviews"

    def reject_reviews(self, request, queryset):
        queryset.update(status='rejected')
    reject_reviews.short_description = "Reject selected reviews"
from django.contrib import admin
from apps.travel_plans.models import TravelPlan, TravelPlanItem


class TravelPlanItemInline(admin.TabularInline):
    model  = TravelPlanItem
    extra  = 0
    fields = ['place', 'day', 'order', 'visit_time', 'duration_hours', 'estimated_cost']
    raw_id_fields = ['place']


@admin.register(TravelPlan)
class TravelPlanAdmin(admin.ModelAdmin):
    list_display  = ['title', 'visitor', 'start_date', 'end_date', 'visibility', 'created_at']
    list_filter   = ['visibility']
    search_fields = ['title', 'visitor__email']
    raw_id_fields = ['visitor']
    inlines       = [TravelPlanItemInline]
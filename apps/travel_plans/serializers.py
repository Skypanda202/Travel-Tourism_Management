"""Smart Tourism — Travel Plans Serializers."""
from rest_framework import serializers
from apps.travel_plans.models import TravelPlan, TravelPlanItem
from apps.places.serializers import TouristPlaceListSerializer


class TravelPlanItemSerializer(serializers.ModelSerializer):
    place_detail = TouristPlaceListSerializer(source='place', read_only=True)

    class Meta:
        model  = TravelPlanItem
        fields = [
            'id', 'place', 'place_detail', 'day', 'order',
            'visit_time', 'duration_hours', 'notes',
            'transport_to', 'estimated_cost',
        ]


class TravelPlanListSerializer(serializers.ModelSerializer):
    duration_days = serializers.ReadOnlyField()
    item_count    = serializers.SerializerMethodField()

    class Meta:
        model  = TravelPlan
        fields = [
            'id', 'title', 'description', 'start_date', 'end_date',
            'duration_days', 'budget', 'currency', 'visibility',
            'item_count', 'created_at',
        ]

    def get_item_count(self, obj):
        return obj.items.count()


class TravelPlanDetailSerializer(serializers.ModelSerializer):
    items         = TravelPlanItemSerializer(many=True, read_only=True)
    duration_days = serializers.ReadOnlyField()
    total_estimated_cost = serializers.SerializerMethodField()

    class Meta:
        model  = TravelPlan
        fields = [
            'id', 'visitor', 'title', 'description',
            'start_date', 'end_date', 'duration_days',
            'budget', 'currency', 'visibility', 'share_token',
            'items', 'total_estimated_cost', 'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'visitor', 'share_token', 'created_at', 'updated_at']

    def get_total_estimated_cost(self, obj):
        total = sum(item.estimated_cost for item in obj.items.all())
        return float(total)

    def validate(self, attrs):
        if attrs.get('end_date') and attrs.get('start_date'):
            if attrs['end_date'] < attrs['start_date']:
                raise serializers.ValidationError("End date must be after start date.")
        return attrs


class TravelPlanCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model  = TravelPlan
        fields = ['title', 'description', 'start_date', 'end_date', 'budget', 'currency', 'visibility']

    def validate(self, attrs):
        if attrs['end_date'] < attrs['start_date']:
            raise serializers.ValidationError({"end_date": "End date must be after start date."})
        return attrs
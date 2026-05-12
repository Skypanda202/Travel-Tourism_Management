"""
Smart Tourism — Places Serializers
"""
from rest_framework import serializers
from apps.places.models import Category, TouristPlace, PlaceImage, Favorite


class CategorySerializer(serializers.ModelSerializer):
    places_count = serializers.SerializerMethodField()

    class Meta:
        model  = Category
        fields = ['id', 'name', 'slug', 'description', 'icon', 'image', 'is_active', 'sort_order', 'places_count']

    def get_places_count(self, obj):
        return obj.places.filter(status='published').count()


class PlaceImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model  = PlaceImage
        fields = ['id', 'image', 'image_url', 'caption', 'is_cover', 'sort_order']

    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None


class TouristPlaceListSerializer(serializers.ModelSerializer):
    """Compact view for place lists."""
    category_name = serializers.CharField(source='category.name', read_only=True)
    cover_image_url = serializers.SerializerMethodField()
    is_favorited  = serializers.SerializerMethodField()

    class Meta:
        model  = TouristPlace
        fields = [
            'id', 'name', 'slug', 'short_desc', 'category', 'category_name',
            'city', 'country', 'cover_image_url', 'entry_fee', 'is_free',
            'avg_rating', 'total_reviews', 'is_featured', 'is_favorited',
            'latitude', 'longitude',
        ]

    def get_cover_image_url(self, obj):
        request = self.context.get('request')
        if obj.cover_image and request:
            return request.build_absolute_uri(obj.cover_image.url)
        return None

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Favorite.objects.filter(user=request.user, place=obj).exists()
        return False


class TouristPlaceDetailSerializer(serializers.ModelSerializer):
    """Full place detail."""
    category     = CategorySerializer(read_only=True)
    category_id  = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source='category', write_only=True, required=False
    )
    images       = PlaceImageSerializer(many=True, read_only=True)
    tag_list     = serializers.ReadOnlyField()
    cover_image_url  = serializers.SerializerMethodField()
    is_favorited = serializers.SerializerMethodField()
    created_by_name  = serializers.CharField(source='created_by.full_name', read_only=True)

    class Meta:
        model  = TouristPlace
        fields = [
            'id', 'name', 'slug', 'description', 'short_desc',
            'category', 'category_id', 'tags', 'tag_list', 'status',
            'address', 'city', 'state', 'country', 'zip_code',
            'latitude', 'longitude', 'google_maps_url',
            'cover_image', 'cover_image_url', 'images',
            'entry_fee', 'entry_fee_currency', 'is_free',
            'opening_time', 'closing_time', 'open_days', 'best_time_to_visit',
            'avg_rating', 'total_reviews', 'total_visits', 'total_bookings',
            'is_featured', 'is_recommended', 'is_favorited',
            'created_by', 'created_by_name', 'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'slug', 'avg_rating', 'total_reviews', 'total_visits',
                            'total_bookings', 'created_by', 'created_at', 'updated_at']

    def get_cover_image_url(self, obj):
        request = self.context.get('request')
        if obj.cover_image and request:
            return request.build_absolute_uri(obj.cover_image.url)
        return None

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Favorite.objects.filter(user=request.user, place=obj).exists()
        return False


class FavoriteSerializer(serializers.ModelSerializer):
    place = TouristPlaceListSerializer(read_only=True)

    class Meta:
        model  = Favorite
        fields = ['id', 'place', 'created_at']


class DistanceSerializer(serializers.Serializer):
    """Input for distance calculation."""
    lat1 = serializers.FloatField()
    lon1 = serializers.FloatField()
    lat2 = serializers.FloatField()
    lon2 = serializers.FloatField()
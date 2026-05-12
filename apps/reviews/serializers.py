"""Smart Tourism — Reviews Serializers."""
from rest_framework import serializers
from apps.reviews.models import Review, ReviewImage
from apps.users.serializers import UserListSerializer


class ReviewImageSerializer(serializers.ModelSerializer):
    class Meta:
        model  = ReviewImage
        fields = ['id', 'image', 'uploaded_at']


class ReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Review
        fields = [
            'place', 'booking', 'rating', 'title', 'content',
            'cleanliness_rating', 'accessibility_rating', 'value_rating',
        ]

    def validate_rating(self, value):
        if not 1 <= value <= 5:
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value

    def validate(self, attrs):
        user  = self.context['request'].user
        place = attrs['place']
        if Review.objects.filter(user=user, place=place).exists():
            raise serializers.ValidationError("You have already reviewed this place.")
        return attrs


class ReviewListSerializer(serializers.ModelSerializer):
    user_name  = serializers.CharField(source='user.full_name', read_only=True)
    place_name = serializers.CharField(source='place.name',     read_only=True)
    images     = ReviewImageSerializer(many=True, read_only=True)

    class Meta:
        model  = Review
        fields = [
            'id', 'user', 'user_name', 'place', 'place_name',
            'rating', 'title', 'content', 'is_verified', 'helpful_count',
            'status', 'images', 'created_at',
        ]


class ReviewDetailSerializer(serializers.ModelSerializer):
    user   = UserListSerializer(read_only=True)
    images = ReviewImageSerializer(many=True, read_only=True)

    class Meta:
        model  = Review
        fields = '__all__'
        read_only_fields = ['id', 'user', 'is_verified', 'helpful_count', 'created_at', 'updated_at']
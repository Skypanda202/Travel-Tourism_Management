"""
Smart Tourism — User Serializers
"""
from django.contrib.auth.password_validation import validate_password
from django.utils import timezone
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from apps.users.models import User, VisitorProfile


# ── Auth Serializers ──────────────────────────────────────────────────────────

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Enrich JWT payload with user info."""

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        is_admin = user.is_admin
        # Add custom claims
        token['email']      = user.email
        token['full_name']  = user.full_name
        token['role']       = 'admin' if is_admin else user.role
        token['is_admin']   = is_admin
        token['is_staff']   = user.is_staff
        token['is_superuser'] = user.is_superuser
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        # Include user details alongside tokens
        data['user'] = UserDetailSerializer(self.user).data
        return data


class RegisterSerializer(serializers.ModelSerializer):
    """Visitor self-registration."""
    password         = serializers.CharField(write_only=True, min_length=8, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'phone_number', 'password', 'confirm_password',
        ]
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name':  {'required': True},
        }

    def validate(self, attrs):
        if attrs['password'] != attrs.pop('confirm_password'):
            raise serializers.ValidationError({"confirm_password": "Passwords do not match."})
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            phone_number=validated_data.get('phone_number', ''),
            password=validated_data['password'],
            role='visitor',
        )
        # Create visitor profile
        VisitorProfile.objects.create(user=user)
        return user


class ChangePasswordSerializer(serializers.Serializer):
    old_password     = serializers.CharField(required=True)
    new_password     = serializers.CharField(required=True, min_length=8, validators=[validate_password])
    confirm_password = serializers.CharField(required=True)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"confirm_password": "Passwords do not match."})
        return attrs


# ── User Serializers ──────────────────────────────────────────────────────────

class UserListSerializer(serializers.ModelSerializer):
    """Compact user representation for lists."""
    full_name  = serializers.ReadOnlyField()
    avatar_url = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'full_name', 'role', 'avatar_url', 'is_active', 'created_at']

    def get_avatar_url(self, obj):
        request = self.context.get('request')
        if obj.avatar and request:
            return request.build_absolute_uri(obj.avatar.url)
        return None


class UserDetailSerializer(serializers.ModelSerializer):
    """Full user detail including profile."""
    full_name  = serializers.ReadOnlyField()
    is_admin   = serializers.ReadOnlyField()
    avatar_url = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name', 'full_name',
            'phone_number', 'avatar', 'avatar_url', 'bio', 'date_of_birth',
            'city', 'country', 'latitude', 'longitude',
            'role', 'is_admin', 'is_verified', 'is_active',
            'preferred_language', 'newsletter_opt_in',
            'date_joined', 'last_login', 'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'role', 'is_verified', 'date_joined', 'last_login', 'created_at', 'updated_at']

    def get_avatar_url(self, obj):
        request = self.context.get('request')
        if obj.avatar and request:
            return request.build_absolute_uri(obj.avatar.url)
        return None


class UserUpdateSerializer(serializers.ModelSerializer):
    """Profile update (visitors updating their own profile)."""
    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'phone_number', 'avatar',
            'bio', 'date_of_birth', 'city', 'country',
            'latitude', 'longitude', 'preferred_language', 'newsletter_opt_in',
        ]


class VisitorProfileSerializer(serializers.ModelSerializer):
    """Visitor preferences."""
    class Meta:
        model  = VisitorProfile
        fields = [
            'id', 'travel_style', 'preferred_categories',
            'total_bookings', 'total_reviews', 'total_places_visited',
            'instagram_handle', 'twitter_handle', 'created_at',
        ]
        read_only_fields = ['id', 'total_bookings', 'total_reviews', 'total_places_visited', 'created_at']


class AdminUserSerializer(serializers.ModelSerializer):
    """Admin-only: create/update any user including role."""
    password = serializers.CharField(write_only=True, required=False, min_length=8)

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'phone_number', 'role', 'is_active', 'is_staff', 'is_verified',
            'password', 'city', 'country', 'created_at',
        ]
        read_only_fields = ['id', 'created_at']

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = User(**validated_data)
        if password:
            user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance

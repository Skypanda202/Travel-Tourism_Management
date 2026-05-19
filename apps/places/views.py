"""
Smart Tourism — Places Views
CRUD for TouristPlace, Category, Favorites, Distance, Weather, Nearby
"""
import logging
import requests
from django.conf import settings
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from apps.places.models import Category, TouristPlace, PlaceImage, Favorite
from apps.places.serializers import (
    CategorySerializer,
    TouristPlaceListSerializer,
    TouristPlaceDetailSerializer,
    PlaceImageSerializer,
    FavoriteSerializer,
)
from smart_tourism.exceptions import success_response, error_response, created_response
from smart_tourism.pagination import StandardResultsPagination
from smart_tourism.permissions import IsAdmin, IsAdminOrReadOnly, IsAuthenticatedOrReadOnly

logger = logging.getLogger(__name__)


class CategoryViewSet(viewsets.ModelViewSet):
    """
    GET    /api/v1/places/categories/        — list categories
    POST   /api/v1/places/categories/        — create (admin)
    GET    /api/v1/places/categories/{id}/   — detail
    PUT    /api/v1/places/categories/{id}/   — update (admin)
    DELETE /api/v1/places/categories/{id}/   — delete (admin)
    """
    queryset           = Category.objects.all()
    serializer_class   = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends    = [filters.SearchFilter, filters.OrderingFilter]
    search_fields      = ['name', 'description']
    ordering_fields    = ['name', 'sort_order']

    def get_queryset(self):
        qs = super().get_queryset()
        if not (self.request.user.is_authenticated and self.request.user.is_admin):
            qs = qs.filter(is_active=True)
        return qs


class TouristPlaceViewSet(viewsets.ModelViewSet):
    """
    Full CRUD for tourist places.
    Public GET; Admin POST/PUT/DELETE.
    Supports: search, filter by category/city/country/status,
              ordering, weather info, nearby places, distance.
    """
    queryset           = TouristPlace.objects.select_related('category', 'created_by').prefetch_related('images')
    permission_classes = [IsAdminOrReadOnly]
    pagination_class   = StandardResultsPagination
    filter_backends    = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields   = ['category', 'city', 'country', 'status', 'is_featured', 'is_free', 'is_recommended']
    search_fields      = ['name', 'description', 'city', 'country', 'tags', 'address']
    ordering_fields    = ['name', 'avg_rating', 'total_reviews', 'entry_fee', 'created_at', 'total_visits']
    lookup_field       = 'slug'

    def get_serializer_class(self):
        if self.action == 'list':
            return TouristPlaceListSerializer
        return TouristPlaceDetailSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        # Non-admin users only see published places
        if not (self.request.user.is_authenticated and self.request.user.is_admin):
            qs = qs.filter(status='published')

        # Price range filter
        min_fee = self.request.query_params.get('min_fee')
        max_fee = self.request.query_params.get('max_fee')
        if min_fee:
            qs = qs.filter(entry_fee__gte=min_fee)
        if max_fee:
            qs = qs.filter(entry_fee__lte=max_fee)

        # Rating filter
        min_rating = self.request.query_params.get('min_rating')
        if min_rating:
            qs = qs.filter(avg_rating__gte=min_rating)

        return qs

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, status='published')
        logger.info("Place created by %s: %s", self.request.user.email, serializer.instance.name)

    def perform_update(self, serializer):
        serializer.save()
        logger.info("Place updated: %s", serializer.instance.name)

    def retrieve(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        return success_response(data=serializer.data)

    # ── Custom actions ─────────────────────────────────────────────────────────

    @action(detail=True, methods=['get'], permission_classes=[AllowAny])
    def weather(self, request, slug=None):
        """
        GET /api/v1/places/{slug}/weather/
        Fetch live weather from OpenWeatherMap API.
        """
        place = self.get_object()
        api_key = settings.WEATHER_API_KEY
        if not api_key:
            return error_response("Weather API key not configured.")

        try:
            resp = requests.get(
                settings.WEATHER_API_URL,
                params={
                    'lat':   float(place.latitude),
                    'lon':   float(place.longitude),
                    'appid': api_key,
                    'units': 'metric',
                },
                timeout=5,
            )
            resp.raise_for_status()
            data = resp.json()
            weather = {
                'city':        data.get('name'),
                'temperature': data['main']['temp'],
                'feels_like':  data['main']['feels_like'],
                'humidity':    data['main']['humidity'],
                'description': data['weather'][0]['description'],
                'icon':        f"https://openweathermap.org/img/wn/{data['weather'][0]['icon']}@2x.png",
                'wind_speed':  data['wind']['speed'],
            }
            return success_response(data=weather)
        except requests.exceptions.RequestException as e:
            logger.warning("Weather API error for place %s: %s", place.name, e)
            return error_response("Could not fetch weather data.", status_code=status.HTTP_503_SERVICE_UNAVAILABLE)

    @action(detail=True, methods=['get'], permission_classes=[AllowAny])
    def nearby(self, request, slug=None):
        """
        GET /api/v1/places/{slug}/nearby/?radius=50
        Return nearby places within radius km (Haversine approximation via DB).
        """
        from math import radians, cos
        place  = self.get_object()
        radius = float(request.query_params.get('radius', 50))   # km
        lat    = float(place.latitude)
        lon    = float(place.longitude)

        # Bounding box approximation
        lat_delta = radius / 111.0
        lon_delta = radius / (111.0 * cos(radians(lat)))

        nearby = TouristPlace.objects.filter(
            status='published',
            latitude__range=(lat - lat_delta, lat + lat_delta),
            longitude__range=(lon - lon_delta, lon + lon_delta),
        ).exclude(pk=place.pk)[:10]

        serializer = TouristPlaceListSerializer(nearby, many=True, context={'request': request})
        return success_response(data=serializer.data)

    @action(detail=False, methods=['get'], permission_classes=[AllowAny])
    def featured(self, request):
        """GET /api/v1/places/featured/ — featured places."""
        places = TouristPlace.objects.filter(status='published', is_featured=True)[:8]
        serializer = TouristPlaceListSerializer(places, many=True, context={'request': request})
        return success_response(data=serializer.data)

    @action(detail=False, methods=['get'], permission_classes=[AllowAny])
    def recommended(self, request):
        """GET /api/v1/places/recommended/ — recommended places."""
        places = TouristPlace.objects.filter(status='published', is_recommended=True).order_by('-avg_rating')[:10]
        serializer = TouristPlaceListSerializer(places, many=True, context={'request': request})
        return success_response(data=serializer.data)

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def distance(self, request):
        """
        POST /api/v1/places/distance/
        Body: { "lat1": ..., "lon1": ..., "lat2": ..., "lon2": ... }
        Returns distance in km using Haversine formula.
        """
        from geopy.distance import geodesic
        try:
            lat1 = float(request.data['lat1'])
            lon1 = float(request.data['lon1'])
            lat2 = float(request.data['lat2'])
            lon2 = float(request.data['lon2'])
        except (KeyError, ValueError):
            return error_response("Provide lat1, lon1, lat2, lon2 as numeric values.")

        dist_km = geodesic((lat1, lon1), (lat2, lon2)).km
        return success_response(data={
            'distance_km':    round(dist_km, 2),
            'distance_miles': round(dist_km * 0.621371, 2),
        })

    @action(detail=True, methods=['post', 'delete'], permission_classes=[IsAuthenticated])
    def favorite(self, request, slug=None):
        """Toggle favorite for authenticated visitor."""
        place = self.get_object()
        fav, created = Favorite.objects.get_or_create(user=request.user, place=place)
        if not created:
            fav.delete()
            return success_response(message="Removed from favorites.", data={'is_favorited': False})
        return success_response(message="Added to favorites.", data={'is_favorited': True})

    @action(detail=True, methods=['post'], permission_classes=[IsAdmin])
    def upload_images(self, request, slug=None):
        """POST multiple images for a place (admin)."""
        place  = self.get_object()
        images = request.FILES.getlist('images')
        if not images:
            return error_response("No images provided.")

        created = []
        for img in images:
            pi = PlaceImage.objects.create(place=place, image=img)
            created.append(PlaceImageSerializer(pi, context={'request': request}).data)

        return created_response(data=created, message=f"{len(created)} image(s) uploaded.")

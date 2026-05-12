"""Smart Tourism — Reviews Views."""
import logging
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny

from apps.reviews.models import Review, ReviewImage
from apps.reviews.serializers import ReviewCreateSerializer, ReviewListSerializer, ReviewDetailSerializer
from smart_tourism.exceptions import success_response, error_response
from smart_tourism.pagination import StandardResultsPagination
from smart_tourism.permissions import IsAdmin, IsOwnerOrAdmin

logger = logging.getLogger(__name__)


class ReviewViewSet(viewsets.ModelViewSet):
    """Reviews API — create, list, moderate."""
    pagination_class = StandardResultsPagination
    filter_backends  = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['place', 'user', 'rating', 'status', 'is_verified']
    search_fields    = ['content', 'title', 'user__email', 'place__name']
    ordering_fields  = ['created_at', 'rating', 'helpful_count']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        if self.action in ['update', 'partial_update', 'destroy', 'approve', 'reject']:
            return [IsAdmin()]
        return [IsAuthenticated()]

    def get_queryset(self):
        qs = Review.objects.select_related('user', 'place').prefetch_related('images')
        user = self.request.user
        # Visitors see only approved reviews; admins see all
        if not (user.is_authenticated and user.is_admin):
            qs = qs.filter(status='approved')
        return qs

    def get_serializer_class(self):
        if self.action == 'create':
            return ReviewCreateSerializer
        if self.action == 'list':
            return ReviewListSerializer
        return ReviewDetailSerializer

    def perform_create(self, serializer):
        review = serializer.save(user=self.request.user)
        logger.info("Review created by %s for place %s", self.request.user.email, review.place.name)

    def perform_destroy(self, instance):
        instance.status = 'rejected'
        instance.save()

    @action(detail=True, methods=['post'], permission_classes=[IsAdmin])
    def approve(self, request, pk=None):
        review = self.get_object()
        review.status = 'approved'
        review.save()
        return success_response(message="Review approved.")

    @action(detail=True, methods=['post'], permission_classes=[IsAdmin])
    def reject(self, request, pk=None):
        review = self.get_object()
        review.status = 'rejected'
        review.save()
        return success_response(message="Review rejected.")

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def mark_helpful(self, request, pk=None):
        review = self.get_object()
        Review.objects.filter(pk=review.pk).update(helpful_count=review.helpful_count + 1)
        return success_response(message="Marked as helpful.")

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def upload_images(self, request, pk=None):
        review = self.get_object()
        images = request.FILES.getlist('images')
        if not images:
            return error_response("No images provided.")
        for img in images:
            ReviewImage.objects.create(review=review, image=img)
        return success_response(message=f"{len(images)} image(s) uploaded.")
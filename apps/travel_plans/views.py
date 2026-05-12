"""Smart Tourism — Travel Plans Views."""
import logging
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny

from apps.travel_plans.models import TravelPlan, TravelPlanItem
from apps.travel_plans.serializers import (
    TravelPlanCreateSerializer,
    TravelPlanListSerializer,
    TravelPlanDetailSerializer,
    TravelPlanItemSerializer,
)
from smart_tourism.exceptions import success_response, error_response, created_response
from smart_tourism.pagination import StandardResultsPagination
from smart_tourism.permissions import IsOwnerOrAdmin

logger = logging.getLogger(__name__)


class TravelPlanViewSet(viewsets.ModelViewSet):
    """
    Travel plan CRUD for visitors.
    GET    /api/v1/travel-plans/               — list own plans
    POST   /api/v1/travel-plans/               — create plan
    GET    /api/v1/travel-plans/{id}/          — detail
    PUT    /api/v1/travel-plans/{id}/          — update
    DELETE /api/v1/travel-plans/{id}/          — delete
    POST   /api/v1/travel-plans/{id}/add-item/ — add a place to plan
    DELETE /api/v1/travel-plans/{id}/remove-item/{item_id}/ — remove item
    GET    /api/v1/travel-plans/shared/{token}/ — public shared plan
    """
    permission_classes = [IsAuthenticated]
    pagination_class   = StandardResultsPagination

    def get_queryset(self):
        user = self.request.user
        if user.is_admin:
            return TravelPlan.objects.all().prefetch_related('items__place')
        return TravelPlan.objects.filter(visitor=user).prefetch_related('items__place')

    def get_serializer_class(self):
        if self.action == 'create':
            return TravelPlanCreateSerializer
        if self.action == 'list':
            return TravelPlanListSerializer
        return TravelPlanDetailSerializer

    def perform_create(self, serializer):
        plan = serializer.save(visitor=self.request.user)
        logger.info("Travel plan '%s' created by %s", plan.title, self.request.user.email)

    def get_object(self):
        obj = super().get_object()
        # Allow owner or admin
        if not (self.request.user.is_admin or obj.visitor == self.request.user):
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("You do not have permission to access this plan.")
        return obj

    # ── Item management ───────────────────────────────────────────────────────

    @action(detail=True, methods=['post'], url_path='add-item')
    def add_item(self, request, pk=None):
        """POST /api/v1/travel-plans/{id}/add-item/"""
        plan       = self.get_object()
        serializer = TravelPlanItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        item = serializer.save(plan=plan)
        return created_response(
            data=TravelPlanItemSerializer(item).data,
            message="Place added to travel plan."
        )

    @action(detail=True, methods=['delete'], url_path=r'remove-item/(?P<item_id>\d+)')
    def remove_item(self, request, pk=None, item_id=None):
        """DELETE /api/v1/travel-plans/{id}/remove-item/{item_id}/"""
        plan = self.get_object()
        try:
            item = plan.items.get(pk=item_id)
            item.delete()
            return success_response(message="Item removed from travel plan.")
        except TravelPlanItem.DoesNotExist:
            return error_response("Item not found in this plan.", status_code=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['post'], url_path='reorder-items')
    def reorder_items(self, request, pk=None):
        """
        POST /api/v1/travel-plans/{id}/reorder-items/
        Body: { "items": [{"id": 1, "day": 1, "order": 0}, ...] }
        """
        plan  = self.get_object()
        items = request.data.get('items', [])
        for item_data in items:
            TravelPlanItem.objects.filter(pk=item_data['id'], plan=plan).update(
                day=item_data.get('day', 1),
                order=item_data.get('order', 0),
            )
        return success_response(message="Items reordered.")

    @action(detail=True, methods=['post'], url_path='make-public')
    def make_public(self, request, pk=None):
        plan = self.get_object()
        plan.visibility = 'shared'
        plan.save()
        return success_response(
            data={'share_token': plan.share_token, 'share_url': f"/api/v1/travel-plans/shared/{plan.share_token}/"},
            message="Travel plan is now publicly shareable."
        )

    @action(detail=False, methods=['get'], url_path=r'shared/(?P<token>[a-f0-9]+)',
            permission_classes=[AllowAny])
    def shared(self, request, token=None):
        """GET /api/v1/travel-plans/shared/{token}/ — public view."""
        try:
            plan = TravelPlan.objects.get(share_token=token, visibility='shared')
        except TravelPlan.DoesNotExist:
            return error_response("Shared plan not found.", status_code=status.HTTP_404_NOT_FOUND)
        return success_response(data=TravelPlanDetailSerializer(plan, context={'request': request}).data)
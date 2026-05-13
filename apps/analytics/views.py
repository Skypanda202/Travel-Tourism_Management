"""
Smart Tourism — Analytics Views
Admin-only analytics dashboard with day/month/year drill-down and export.
"""
import csv
import io
import logging
from datetime import date, timedelta

from django.db.models import Sum, Count, Avg
from django.http import HttpResponse
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.analytics.models import DailyAnalytics, PlaceAnalytics, VisitorActivity
from apps.analytics.serializers import (
    DailyAnalyticsSerializer,
    PlaceAnalyticsSerializer,
    VisitorActivitySerializer,
)
from smart_tourism.exceptions import success_response, error_response
from smart_tourism.pagination import StandardResultsPagination, LargeResultsPagination
from smart_tourism.permissions import IsAdmin

logger = logging.getLogger(__name__)


class AnalyticsViewSet(viewsets.GenericViewSet):
    """
    Admin analytics endpoints.

    GET /api/v1/analytics/dashboard/        — high-level KPIs
    GET /api/v1/analytics/daily/            — day-wise (range or single date)
    GET /api/v1/analytics/monthly/          — month-wise (?year=2025)
    GET /api/v1/analytics/yearly/           — year-wise
    GET /api/v1/analytics/places/           — per-place stats
    GET /api/v1/analytics/top-places/       — top 10 places by metric
    GET /api/v1/analytics/revenue/          — revenue breakdown
    GET /api/v1/analytics/visitors/         — recent visitor activities
    POST /api/v1/analytics/trigger/         — manually trigger aggregation
    GET /api/v1/analytics/export/bookings/  — CSV export
    GET /api/v1/analytics/export/revenue/   — CSV export
    """
    permission_classes = [IsAdmin]
    pagination_class   = StandardResultsPagination

    # ── Dashboard ─────────────────────────────────────────────────────────────

    @action(detail=False, methods=['get'])
    def dashboard(self, request):
        """Overall KPIs for the admin dashboard."""
        from apps.bookings.models import Booking
        from apps.cabs.models import CabBooking
        from apps.payments.models import Payment
        from apps.reviews.models import Review
        from apps.users.models import User
        from apps.places.models import TouristPlace

        today        = date.today()
        month_start  = today.replace(day=1)
        year_start   = today.replace(month=1, day=1)
        yesterday    = today - timedelta(days=1)

        paid = Payment.objects.filter(status='success')

        kpis = {
            # Users
            'total_users':          User.objects.filter(role='visitor').count(),
            'new_users_today':      User.objects.filter(date_joined__date=today).count(),
            'new_users_this_month': User.objects.filter(date_joined__date__gte=month_start).count(),

            # Places
            'total_places':     TouristPlace.objects.filter(status='published').count(),
            'featured_places':  TouristPlace.objects.filter(is_featured=True).count(),

            # Bookings
            'total_bookings':       Booking.objects.count(),
            'bookings_today':       Booking.objects.filter(created_at__date=today).count(),
            'bookings_this_month':  Booking.objects.filter(created_at__date__gte=month_start).count(),
            'pending_bookings':     Booking.objects.filter(status='pending').count(),

            # Cabs
            'cab_bookings_today':  CabBooking.objects.filter(created_at__date=today).count(),

            # Revenue
            'revenue_today':       float(paid.filter(completed_at__date=today).aggregate(t=Sum('net_amount'))['t'] or 0),
            'revenue_this_month':  float(paid.filter(completed_at__date__gte=month_start).aggregate(t=Sum('net_amount'))['t'] or 0),
            'revenue_this_year':   float(paid.filter(completed_at__date__gte=year_start).aggregate(t=Sum('net_amount'))['t'] or 0),
            'revenue_total':       float(paid.aggregate(t=Sum('net_amount'))['t'] or 0),

            # Reviews
            'total_reviews':    Review.objects.filter(status='approved').count(),
            'pending_reviews':  Review.objects.filter(status='pending').count(),
            'avg_platform_rating': float(
                Review.objects.filter(status='approved').aggregate(a=Avg('rating'))['a'] or 0
            ),
        }
        return success_response(data=kpis)

    # ── Day-wise ──────────────────────────────────────────────────────────────

    @action(detail=False, methods=['get'])
    def daily(self, request):
        """
        GET /api/v1/analytics/daily/?start=YYYY-MM-DD&end=YYYY-MM-DD
        Returns pre-aggregated DailyAnalytics rows for the date range.
        Defaults to last 30 days.
        """
        today      = date.today()
        start_str  = request.query_params.get('start')
        end_str    = request.query_params.get('end')

        try:
            start = date.fromisoformat(start_str) if start_str else today - timedelta(days=29)
            end   = date.fromisoformat(end_str)   if end_str   else today
        except ValueError:
            return error_response("Invalid date format. Use YYYY-MM-DD.")

        rows = DailyAnalytics.objects.filter(date__range=(start, end)).order_by('date')
        serializer = DailyAnalyticsSerializer(rows, many=True)
        return success_response(data={
            'start': str(start), 'end': str(end),
            'days':  len(serializer.data),
            'rows':  serializer.data,
        })

    # ── Month-wise ────────────────────────────────────────────────────────────

    @action(detail=False, methods=['get'])
    def monthly(self, request):
        """
        GET /api/v1/analytics/monthly/?year=2025
        Aggregates DailyAnalytics rows by month for the given year.
        """
        year = int(request.query_params.get('year', date.today().year))

        rows = (
            DailyAnalytics.objects
            .filter(date__year=year)
            .extra(select={'month': "MONTH(date)"})
            .values('month')
            .annotate(
                total_visits=Sum('total_visits'),
                unique_visitors=Sum('unique_visitors'),
                new_registrations=Sum('new_registrations'),
                total_bookings=Sum('total_bookings'),
                confirmed_bookings=Sum('confirmed_bookings'),
                cancelled_bookings=Sum('cancelled_bookings'),
                cab_bookings=Sum('cab_bookings'),
                booking_revenue=Sum('booking_revenue'),
                cab_revenue=Sum('cab_revenue'),
                total_revenue=Sum('total_revenue'),
                total_reviews=Sum('total_reviews'),
            )
            .order_by('month')
        )

        # Add month names
        import calendar
        data = []
        for row in rows:
            row['month_name'] = calendar.month_name[row['month']]
            row['total_revenue'] = float(row['total_revenue'] or 0)
            row['booking_revenue'] = float(row['booking_revenue'] or 0)
            row['cab_revenue'] = float(row['cab_revenue'] or 0)
            data.append(row)

        return success_response(data={'year': year, 'months': data})

    # ── Year-wise ─────────────────────────────────────────────────────────────

    @action(detail=False, methods=['get'])
    def yearly(self, request):
        """
        GET /api/v1/analytics/yearly/
        Aggregates by year across all DailyAnalytics rows.
        """
        rows = (
            DailyAnalytics.objects
            .extra(select={'year': "YEAR(date)"})
            .values('year')
            .annotate(
                total_visits=Sum('total_visits'),
                unique_visitors=Sum('unique_visitors'),
                new_registrations=Sum('new_registrations'),
                total_bookings=Sum('total_bookings'),
                cab_bookings=Sum('cab_bookings'),
                total_revenue=Sum('total_revenue'),
                total_reviews=Sum('total_reviews'),
            )
            .order_by('year')
        )

        data = []
        for row in rows:
            row['total_revenue'] = float(row['total_revenue'] or 0)
            data.append(row)

        return success_response(data={'years': data})

    # ── Per-place stats ───────────────────────────────────────────────────────

    @action(detail=False, methods=['get'])
    def places(self, request):
        """
        GET /api/v1/analytics/places/?place_id=&start=&end=
        Per-place analytics for a date range.
        """
        today     = date.today()
        start_str = request.query_params.get('start')
        end_str   = request.query_params.get('end')
        place_id  = request.query_params.get('place_id')

        try:
            start = date.fromisoformat(start_str) if start_str else today - timedelta(days=29)
            end   = date.fromisoformat(end_str)   if end_str   else today
        except ValueError:
            return error_response("Invalid date format.")

        qs = PlaceAnalytics.objects.filter(date__range=(start, end)).select_related('place')
        if place_id:
            qs = qs.filter(place_id=place_id)

        serializer = PlaceAnalyticsSerializer(qs, many=True)
        return success_response(data=serializer.data)

    # ── Top places ────────────────────────────────────────────────────────────

    @action(detail=False, methods=['get'], url_path='top-places')
    def top_places(self, request):
        """
        GET /api/v1/analytics/top-places/?metric=bookings&limit=10
        metric: bookings | views | revenue | reviews | favorites
        """
        metric = request.query_params.get('metric', 'bookings')
        limit  = min(int(request.query_params.get('limit', 10)), 50)

        METRIC_MAP = {
            'bookings': 'total_bookings',
            'views':    'views',
            'revenue':  'revenue',
            'reviews':  'reviews',
            'favorites': 'favorites',
        }
        agg_field = METRIC_MAP.get(metric, 'total_bookings')

        rows = (
            PlaceAnalytics.objects
            .values('place__id', 'place__name', 'place__city')
            .annotate(total=Sum(agg_field))
            .order_by('-total')[:limit]
        )

        data = [
            {
                'place_id':   r['place__id'],
                'place_name': r['place__name'],
                'city':       r['place__city'],
                'metric':     metric,
                'value':      float(r['total'] or 0),
            }
            for r in rows
        ]
        return success_response(data=data)

    # ── Revenue report ────────────────────────────────────────────────────────

    @action(detail=False, methods=['get'])
    def revenue(self, request):
        """
        GET /api/v1/analytics/revenue/?start=&end=
        Detailed revenue breakdown.
        """
        from apps.payments.models import Payment
        today     = date.today()
        start_str = request.query_params.get('start')
        end_str   = request.query_params.get('end')

        try:
            start = date.fromisoformat(start_str) if start_str else today.replace(day=1)
            end   = date.fromisoformat(end_str)   if end_str   else today
        except ValueError:
            return error_response("Invalid date format.")

        paid = Payment.objects.filter(status='success', completed_at__date__range=(start, end))

        data = {
            'period':          {'start': str(start), 'end': str(end)},
            'total_revenue':   float(paid.aggregate(t=Sum('net_amount'))['t'] or 0),
            'booking_revenue': float(paid.filter(payment_type='booking').aggregate(t=Sum('net_amount'))['t'] or 0),
            'cab_revenue':     float(paid.filter(payment_type='cab_booking').aggregate(t=Sum('net_amount'))['t'] or 0),
            'by_method': list(
                paid.values('payment_method')
                    .annotate(count=Count('id'), amount=Sum('net_amount'))
                    .order_by('-amount')
            ),
            'daily_trend': list(
                paid.extra(select={'day': "DATE(completed_at)"})
                    .values('day')
                    .annotate(revenue=Sum('net_amount'), transactions=Count('id'))
                    .order_by('day')
            ),
        }
        # Serialise Decimal → float for JSON
        for row in data['by_method']:
            row['amount'] = float(row['amount'] or 0)
        for row in data['daily_trend']:
            row['revenue'] = float(row['revenue'] or 0)

        return success_response(data=data)

    # ── Visitor activity log ──────────────────────────────────────────────────

    @action(detail=False, methods=['get'])
    def visitors(self, request):
        """
        GET /api/v1/analytics/visitors/?user_id=&action=&limit=100
        Recent raw activity log.
        """
        qs = VisitorActivity.objects.select_related('user').order_by('-created_at')

        user_id = request.query_params.get('user_id')
        action  = request.query_params.get('action')
        limit   = min(int(request.query_params.get('limit', 50)), 500)

        if user_id:
            qs = qs.filter(user_id=user_id)
        if action:
            qs = qs.filter(action=action)

        qs = qs[:limit]
        serializer = VisitorActivitySerializer(qs, many=True)
        return success_response(data=serializer.data)

    # ── Manual trigger ────────────────────────────────────────────────────────

    @action(detail=False, methods=['post'])
    def trigger(self, request):
        """
        POST /api/v1/analytics/trigger/
        Body: { "date": "YYYY-MM-DD" }   (optional, defaults to yesterday)
        Manually fires the aggregation tasks (admin convenience).
        """
        from apps.analytics.tasks import aggregate_daily_analytics, aggregate_place_analytics
        target = request.data.get('date')
        aggregate_daily_analytics.delay(target)
        aggregate_place_analytics.delay(target)
        return success_response(message=f"Aggregation tasks queued for {target or 'yesterday'}.")

    # ── CSV Exports ───────────────────────────────────────────────────────────

    @action(detail=False, methods=['get'], url_path='export/bookings')
    def export_bookings(self, request):
        """
        GET /api/v1/analytics/export/bookings/?start=&end=
        Download bookings as CSV.
        """
        from apps.bookings.models import Booking
        today     = date.today()
        start_str = request.query_params.get('start')
        end_str   = request.query_params.get('end')

        try:
            start = date.fromisoformat(start_str) if start_str else today.replace(day=1)
            end   = date.fromisoformat(end_str)   if end_str   else today
        except ValueError:
            return error_response("Invalid date format.")

        bookings = Booking.objects.filter(
            created_at__date__range=(start, end)
        ).select_related('visitor', 'place').order_by('created_at')

        # Build CSV in memory
        buf    = io.StringIO()
        writer = csv.writer(buf)
        writer.writerow([
            'Booking Ref', 'Visitor Email', 'Visitor Name', 'Place',
            'City', 'Visit Date', 'Adults', 'Children',
            'Total Amount', 'Currency', 'Status', 'Payment Status', 'Created At'
        ])
        for b in bookings:
            writer.writerow([
                b.booking_ref, b.visitor.email, b.visitor.full_name,
                b.place.name, b.place.city, b.visit_date,
                b.num_adults, b.num_children, b.total_amount, b.currency,
                b.status, b.payment_status, b.created_at.strftime('%Y-%m-%d %H:%M')
            ])

        response = HttpResponse(buf.getvalue(), content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="bookings_{start}_{end}.csv"'
        return response

    @action(detail=False, methods=['get'], url_path='export/revenue')
    def export_revenue(self, request):
        """
        GET /api/v1/analytics/export/revenue/?start=&end=
        Download revenue report as CSV.
        """
        from apps.payments.models import Payment
        today     = date.today()
        start_str = request.query_params.get('start')
        end_str   = request.query_params.get('end')

        try:
            start = date.fromisoformat(start_str) if start_str else today.replace(day=1)
            end   = date.fromisoformat(end_str)   if end_str   else today
        except ValueError:
            return error_response("Invalid date format.")

        payments = Payment.objects.filter(
            status='success', completed_at__date__range=(start, end)
        ).select_related('user').order_by('completed_at')

        buf    = io.StringIO()
        writer = csv.writer(buf)
        writer.writerow([
            'Transaction Ref', 'User Email', 'Payment Type',
            'Booking ID', 'Amount', 'Discount', 'Net Amount',
            'Currency', 'Method', 'Gateway', 'Completed At'
        ])
        for p in payments:
            writer.writerow([
                p.transaction_ref, p.user.email, p.payment_type,
                p.booking_id, p.amount, p.discount, p.net_amount,
                p.currency, p.payment_method, p.gateway,
                p.completed_at.strftime('%Y-%m-%d %H:%M') if p.completed_at else ''
            ])

        response = HttpResponse(buf.getvalue(), content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="revenue_{start}_{end}.csv"'
        return response
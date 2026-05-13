"""
Smart Tourism — Analytics Celery Tasks
- log_visitor_activity : lightweight async activity logger
- aggregate_daily_analytics : nightly cron to roll up stats
- aggregate_place_analytics : nightly per-place roll up
"""
import logging
from datetime import date, timedelta
from celery import shared_task
from django.db.models import Sum, Count, Q

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=2, ignore_result=True)
def log_visitor_activity(self, user_id, action, ip_address='', user_agent='', path=''):
    """Async: persist a VisitorActivity row."""
    try:
        from apps.analytics.models import VisitorActivity
        VisitorActivity.objects.create(
            user_id=user_id,
            action=action,
            ip_address=ip_address or None,
            user_agent=user_agent,
            extra_data={'path': path},
        )
    except Exception as exc:
        logger.error("log_visitor_activity failed: %s", exc)
        raise self.retry(exc=exc, countdown=10)


@shared_task
def aggregate_daily_analytics(target_date_str=None):
    """
    Nightly task: aggregate platform-wide stats for a given date.
    If target_date_str is None, uses yesterday.
    Scheduled via django-celery-beat at 00:05 every day.
    """
    from apps.analytics.models import DailyAnalytics, VisitorActivity
    from apps.bookings.models import Booking
    from apps.cabs.models import CabBooking
    from apps.payments.models import Payment
    from apps.reviews.models import Review
    from apps.users.models import User

    if target_date_str:
        from datetime import datetime
        target = datetime.strptime(target_date_str, '%Y-%m-%d').date()
    else:
        target = date.today() - timedelta(days=1)

    logger.info("Aggregating daily analytics for %s", target)

    # Activity counts
    acts = VisitorActivity.objects.filter(created_at__date=target)
    total_visits    = acts.filter(action__in=['view_place', 'view_page']).count()
    unique_visitors = acts.exclude(user=None).values('user').distinct().count()
    searches        = acts.filter(action='search').count()
    favorites       = acts.filter(action='add_favorite').count()
    new_regs        = User.objects.filter(date_joined__date=target).count()

    # Bookings
    bookings = Booking.objects.filter(created_at__date=target)
    total_bk = bookings.count()
    conf_bk  = bookings.filter(status='confirmed').count()
    canc_bk  = bookings.filter(status='cancelled').count()
    comp_bk  = bookings.filter(status='completed').count()

    # Cab bookings
    cab_bk = CabBooking.objects.filter(created_at__date=target).count()

    # Revenue
    paid_payments = Payment.objects.filter(status='success', completed_at__date=target)
    bk_rev  = paid_payments.filter(payment_type='booking').aggregate(t=Sum('net_amount'))['t'] or 0
    cab_rev = paid_payments.filter(payment_type='cab_booking').aggregate(t=Sum('net_amount'))['t'] or 0

    # Reviews
    rev_count = Review.objects.filter(created_at__date=target).count()

    # Upsert
    DailyAnalytics.objects.update_or_create(
        date=target,
        defaults=dict(
            total_visits=total_visits,
            unique_visitors=unique_visitors,
            new_registrations=new_regs,
            total_bookings=total_bk,
            confirmed_bookings=conf_bk,
            cancelled_bookings=canc_bk,
            completed_bookings=comp_bk,
            cab_bookings=cab_bk,
            booking_revenue=bk_rev,
            cab_revenue=cab_rev,
            total_revenue=float(bk_rev) + float(cab_rev),
            total_reviews=rev_count,
            total_searches=searches,
            total_favorites=favorites,
        )
    )
    logger.info("Daily analytics aggregated for %s: revenue=%.2f", target, float(bk_rev) + float(cab_rev))


@shared_task
def aggregate_place_analytics(target_date_str=None):
    """
    Nightly task: per-place daily stats roll-up.
    """
    from apps.analytics.models import PlaceAnalytics, VisitorActivity
    from apps.bookings.models import Booking
    from apps.reviews.models import Review
    from apps.places.models import Favorite, TouristPlace
    from apps.payments.models import Payment

    if target_date_str:
        from datetime import datetime
        target = datetime.strptime(target_date_str, '%Y-%m-%d').date()
    else:
        target = date.today() - timedelta(days=1)

    logger.info("Aggregating per-place analytics for %s", target)

    for place in TouristPlace.objects.filter(status='published'):
        views    = VisitorActivity.objects.filter(
            created_at__date=target,
            action='view_place',
            resource_type='TouristPlace',
            resource_id=place.pk,
        ).count()

        bookings = Booking.objects.filter(place=place, created_at__date=target).count()
        reviews  = Review.objects.filter(place=place, created_at__date=target).count()
        favs     = VisitorActivity.objects.filter(
            created_at__date=target, action='add_favorite',
            resource_type='TouristPlace', resource_id=place.pk
        ).count()
        revenue  = Payment.objects.filter(
            status='success', payment_type='booking', completed_at__date=target,
            booking_id__in=Booking.objects.filter(place=place).values_list('id', flat=True)
        ).aggregate(t=Sum('net_amount'))['t'] or 0

        PlaceAnalytics.objects.update_or_create(
            place=place, date=target,
            defaults=dict(views=views, bookings=bookings, reviews=reviews, favorites=favs, revenue=revenue)
        )
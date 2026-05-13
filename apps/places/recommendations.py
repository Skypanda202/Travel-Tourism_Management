"""
Smart Tourism — Recommendations Engine
Simple content-based + collaborative filtering using Django ORM.
No ML library required — uses rating aggregates and visit history.
"""
import logging
from django.db.models import Q, Avg, Count

logger = logging.getLogger(__name__)


def get_recommendations_for_user(user, limit=10):
    """
    Returns recommended TouristPlace querysets for a visitor.

    Strategy (priority order):
    1. Places in categories the visitor has booked/favorited before
    2. Highly-rated places in cities they have visited
    3. Featured & recommended places they haven't seen yet
    4. Fallback: top-rated published places
    """
    from apps.places.models import TouristPlace, Favorite
    from apps.bookings.models import Booking

    visited_place_ids = set(
        Booking.objects.filter(visitor=user)
        .values_list('place_id', flat=True)
    )
    favorite_place_ids = set(
        Favorite.objects.filter(user=user)
        .values_list('place_id', flat=True)
    )
    seen_ids = visited_place_ids | favorite_place_ids

    base_qs = TouristPlace.objects.filter(status='published').exclude(pk__in=seen_ids)

    # Step 1: preferred categories
    preferred_category_ids = list(
        TouristPlace.objects.filter(pk__in=seen_ids)
        .values_list('category_id', flat=True)
        .distinct()
    )

    results = []
    if preferred_category_ids:
        cat_recs = base_qs.filter(category_id__in=preferred_category_ids) \
                          .order_by('-avg_rating', '-is_featured')[:limit]
        results = list(cat_recs)

    # Step 2: cities visited
    if len(results) < limit:
        visited_cities = list(
            TouristPlace.objects.filter(pk__in=visited_place_ids)
            .values_list('city', flat=True)
            .distinct()
        )
        if visited_cities:
            city_recs = base_qs.filter(city__in=visited_cities) \
                                .exclude(pk__in=[p.pk for p in results]) \
                                .order_by('-avg_rating')[:limit - len(results)]
            results += list(city_recs)

    # Step 3: featured fallback
    if len(results) < limit:
        featured = base_qs.filter(is_featured=True) \
                          .exclude(pk__in=[p.pk for p in results]) \
                          .order_by('-avg_rating')[:limit - len(results)]
        results += list(featured)

    # Step 4: top-rated fallback
    if len(results) < limit:
        top = base_qs.exclude(pk__in=[p.pk for p in results]) \
                     .order_by('-avg_rating', '-total_reviews')[:limit - len(results)]
        results += list(top)

    return results[:limit]


def get_similar_places(place, limit=6):
    """
    Returns places similar to the given place.
    Similarity: same category + same country, ordered by rating.
    """
    from apps.places.models import TouristPlace

    similar = TouristPlace.objects.filter(
        status='published',
        category=place.category,
        country=place.country,
    ).exclude(pk=place.pk).order_by('-avg_rating', '-is_featured')[:limit]

    if similar.count() < limit:
        # Broaden to just same country
        extra = TouristPlace.objects.filter(
            status='published',
            country=place.country,
        ).exclude(
            pk__in=[place.pk] + [p.pk for p in similar]
        ).order_by('-avg_rating')[:limit - similar.count()]
        return list(similar) + list(extra)

    return list(similar)
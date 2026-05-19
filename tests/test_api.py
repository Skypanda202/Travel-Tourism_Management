"""
Smart Tourism — Test Suite
Covers: Auth, Places, Bookings, Reviews, Cabs, Travel Plans
"""
import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status


# ── Fixtures ──────────────────────────────────────────────────────────────────

@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def admin_user(db):
    from django.contrib.auth import get_user_model
    User = get_user_model()
    user = User.objects.create_user(
        username='admin_test',
        email='admin@test.com',
        password='Admin@1234',
        first_name='Admin',
        last_name='User',
        role='admin',
        is_staff=True,
    )
    return user


@pytest.fixture
def visitor_user(db):
    from django.contrib.auth import get_user_model
    from apps.users.models import VisitorProfile
    User = get_user_model()
    user = User.objects.create_user(
        username='visitor_test',
        email='visitor@test.com',
        password='Visitor@1234',
        first_name='Test',
        last_name='Visitor',
        role='visitor',
    )
    VisitorProfile.objects.create(user=user)
    return user


@pytest.fixture
def admin_client(api_client, admin_user):
    client = APIClient()
    client.force_authenticate(user=admin_user)
    return client


@pytest.fixture
def visitor_client(api_client, visitor_user):
    client = APIClient()
    client.force_authenticate(user=visitor_user)
    return client


@pytest.fixture
def category(db, admin_user):
    from apps.places.models import Category
    return Category.objects.create(name='Beach', icon='🏖️', sort_order=1)


@pytest.fixture
def tourist_place(db, category, admin_user):
    from apps.places.models import TouristPlace
    return TouristPlace.objects.create(
        name='Test Beach',
        description='A beautiful test beach.',
        short_desc='Test beach short',
        category=category,
        city='Goa', country='India',
        address='Test Address, Goa',
        latitude='15.5590',
        longitude='73.7590',
        entry_fee='100.00',
        status='published',
        created_by=admin_user,
    )


@pytest.fixture
def cab_type(db):
    from apps.cabs.models import CabType
    return CabType.objects.create(
        name='Sedan', capacity=4,
        price_per_km=15, base_fare=80, is_ac=True,
    )


# ── Auth Tests ────────────────────────────────────────────────────────────────

class TestAuth:

    def test_register_visitor(self, api_client, db):
        data = {
            'username':         'newuser',
            'email':            'new@test.com',
            'first_name':       'New',
            'last_name':        'User',
            'password':         'Secure@1234',
            'confirm_password': 'Secure@1234',
        }
        resp = api_client.post('/api/v1/auth/register/', data)
        assert resp.status_code == status.HTTP_201_CREATED
        assert resp.data['success'] is True
        assert 'access_token' in resp.data

    def test_register_password_mismatch(self, api_client, db):
        data = {
            'username': 'x', 'email': 'x@x.com',
            'first_name': 'X', 'last_name': 'X',
            'password': 'Secure@1234', 'confirm_password': 'Wrong',
        }
        resp = api_client.post('/api/v1/auth/register/', data)
        assert resp.status_code == status.HTTP_400_BAD_REQUEST

    def test_login_success(self, api_client, visitor_user):
        resp = api_client.post('/api/v1/auth/login/', {
            'email': 'visitor@test.com', 'password': 'Visitor@1234'
        })
        assert resp.status_code == status.HTTP_200_OK
        assert 'access_token' in resp.data
        assert resp.data['user']['role'] == 'visitor'

    def test_admin_login_token_marks_admin(self, api_client, admin_user):
        from rest_framework_simplejwt.tokens import AccessToken

        resp = api_client.post('/api/v1/auth/login/', {
            'email': 'admin@test.com', 'password': 'Admin@1234'
        })

        assert resp.status_code == status.HTTP_200_OK
        token = AccessToken(resp.data['access_token'])
        assert token['role'] == 'admin'
        assert token['is_admin'] is True

    def test_staff_user_with_visitor_role_logs_in_as_admin(self, api_client, db):
        from django.contrib.auth import get_user_model
        from rest_framework_simplejwt.tokens import AccessToken

        User = get_user_model()
        user = User.objects.create_user(
            username='legacy_admin',
            email='legacy-admin@test.com',
            password='Admin@1234',
            first_name='Legacy',
            last_name='Admin',
            role='visitor',
            is_staff=True,
            is_superuser=True,
        )

        resp = api_client.post('/api/v1/auth/login/', {
            'email': user.email, 'password': 'Admin@1234'
        })

        assert resp.status_code == status.HTTP_200_OK
        token = AccessToken(resp.data['access_token'])
        assert token['role'] == 'admin'
        assert token['is_admin'] is True

    def test_login_wrong_password(self, api_client, visitor_user):
        resp = api_client.post('/api/v1/auth/login/', {
            'email': 'visitor@test.com', 'password': 'wrong'
        })
        assert resp.status_code == status.HTTP_401_UNAUTHORIZED

    def test_me_endpoint(self, visitor_client, visitor_user):
        resp = visitor_client.get('/api/v1/auth/me/')
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data['data']['email'] == visitor_user.email

    def test_change_password(self, visitor_client):
        resp = visitor_client.post('/api/v1/auth/change-password/', {
            'old_password':     'Visitor@1234',
            'new_password':     'NewPass@5678',
            'confirm_password': 'NewPass@5678',
        })
        assert resp.status_code == status.HTTP_200_OK


# ── Places Tests ──────────────────────────────────────────────────────────────

class TestPlaces:

    def test_list_places_public(self, api_client, tourist_place):
        resp = api_client.get('/api/v1/places/')
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data['pagination']['count'] >= 1

    def test_place_detail(self, api_client, tourist_place):
        resp = api_client.get(f'/api/v1/places/{tourist_place.slug}/')
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data['data']['name'] == 'Test Beach'

    def test_admin_create_place(self, admin_client, category):
        data = {
            'name':        'New Place',
            'description': 'A wonderful new place to visit.',
            'short_desc':  'Short description.',
            'category_id': category.pk,
            'city':        'Mumbai', 'country': 'India',
            'address':     '123 Marine Drive, Mumbai',
            'latitude':    '18.9388',
            'longitude':   '72.8354',
            'entry_fee':   '0.00',
        }
        resp = admin_client.post('/api/v1/places/', data)
        assert resp.status_code == status.HTTP_201_CREATED
        assert resp.data['name'] == 'New Place'

    def test_visitor_cannot_create_place(self, visitor_client, category):
        resp = visitor_client.post('/api/v1/places/', {
            'name': 'Hack', 'description': 'Bad', 'category_id': category.pk,
            'city': 'X', 'country': 'Y', 'address': 'Z',
            'latitude': '0', 'longitude': '0', 'entry_fee': '0',
        })
        assert resp.status_code == status.HTTP_403_FORBIDDEN

    def test_search_places(self, api_client, tourist_place):
        resp = api_client.get('/api/v1/places/?search=Beach')
        assert resp.status_code == status.HTTP_200_OK

    def test_filter_places_by_city(self, api_client, tourist_place):
        resp = api_client.get('/api/v1/places/?city=Goa')
        assert resp.status_code == status.HTTP_200_OK

    def test_distance_calculation(self, api_client):
        resp = api_client.post('/api/v1/places/distance/', {
            'lat1': 28.6139, 'lon1': 77.2090,   # Delhi
            'lat2': 19.0760, 'lon2': 72.8777,   # Mumbai
        })
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data['data']['distance_km'] > 1000

    def test_nearby_places(self, api_client, tourist_place):
        resp = api_client.get(f'/api/v1/places/{tourist_place.slug}/nearby/?radius=100')
        assert resp.status_code == status.HTTP_200_OK

    def test_toggle_favorite(self, visitor_client, tourist_place):
        # Add
        resp = visitor_client.post(f'/api/v1/places/{tourist_place.slug}/favorite/')
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data['data']['is_favorited'] is True
        # Remove
        resp = visitor_client.post(f'/api/v1/places/{tourist_place.slug}/favorite/')
        assert resp.data['data']['is_favorited'] is False

    def test_featured_places(self, api_client, tourist_place):
        resp = api_client.get('/api/v1/places/featured/')
        assert resp.status_code == status.HTTP_200_OK


# ── Categories Tests ──────────────────────────────────────────────────────────

class TestCategories:

    def test_list_categories(self, api_client, category):
        resp = api_client.get('/api/v1/places/categories/')
        assert resp.status_code == status.HTTP_200_OK

    def test_admin_create_category(self, admin_client):
        resp = admin_client.post('/api/v1/places/categories/', {
            'name': 'Adventure', 'description': 'Thrilling adventures'
        })
        assert resp.status_code == status.HTTP_201_CREATED


# ── Bookings Tests ────────────────────────────────────────────────────────────

class TestBookings:

    def test_create_booking(self, visitor_client, tourist_place):
        from datetime import date, timedelta
        resp = visitor_client.post('/api/v1/bookings/', {
            'place':      tourist_place.pk,
            'visit_date': str(date.today() + timedelta(days=7)),
            'num_adults':   2,
            'num_children': 1,
        })
        assert resp.status_code == status.HTTP_201_CREATED
        assert 'booking_ref' in resp.data

    def test_list_own_bookings(self, visitor_client, visitor_user, tourist_place):
        resp = visitor_client.get('/api/v1/bookings/')
        assert resp.status_code == status.HTTP_200_OK

    def test_cancel_booking(self, visitor_client, tourist_place):
        from datetime import date, timedelta
        create_resp = visitor_client.post('/api/v1/bookings/', {
            'place':      tourist_place.pk,
            'visit_date': str(date.today() + timedelta(days=5)),
            'num_adults': 1,
        })
        booking_id = create_resp.data['id']
        cancel_resp = visitor_client.post(f'/api/v1/bookings/{booking_id}/cancel/', {
            'cancel_reason': 'Change of plans'
        })
        assert cancel_resp.status_code == status.HTTP_200_OK

    def test_past_visit_date_rejected(self, visitor_client, tourist_place):
        from datetime import date, timedelta
        resp = visitor_client.post('/api/v1/bookings/', {
            'place':      tourist_place.pk,
            'visit_date': str(date.today() - timedelta(days=1)),
            'num_adults': 1,
        })
        assert resp.status_code == status.HTTP_400_BAD_REQUEST

    def test_admin_sees_all_bookings(self, admin_client, visitor_user, tourist_place):
        resp = admin_client.get('/api/v1/bookings/')
        assert resp.status_code == status.HTTP_200_OK

    def test_booking_stats(self, admin_client):
        resp = admin_client.get('/api/v1/bookings/stats/')
        assert resp.status_code == status.HTTP_200_OK
        assert 'total' in resp.data['data']


# ── Cabs Tests ────────────────────────────────────────────────────────────────

class TestCabs:

    def test_list_cab_types(self, api_client, cab_type):
        resp = api_client.get('/api/v1/cabs/types/')
        assert resp.status_code == status.HTTP_200_OK

    def test_estimate_fare(self, api_client, cab_type):
        resp = api_client.post('/api/v1/cabs/bookings/estimate_fare/', {
            'cab_type_id': cab_type.pk,
            'distance_km': 20,
        })
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data['data']['total_fare'] == 80 + 15 * 20  # base + dist

    def test_create_cab_booking(self, visitor_client, cab_type):
        from datetime import datetime, timedelta
        pickup = (datetime.now() + timedelta(hours=2)).strftime('%Y-%m-%dT%H:%M:00')
        resp = visitor_client.post('/api/v1/cabs/bookings/', {
            'cab_type':        cab_type.pk,
            'pickup_address':  'Hotel A, Goa',
            'dropoff_address': 'Airport, Goa',
            'distance_km':     15,
            'pickup_datetime': pickup,
            'num_passengers':  2,
        })
        assert resp.status_code == status.HTTP_201_CREATED


# ── Reviews Tests ─────────────────────────────────────────────────────────────

class TestReviews:

    def test_create_review(self, visitor_client, tourist_place):
        resp = visitor_client.post('/api/v1/reviews/', {
            'place':   tourist_place.pk,
            'rating':  4,
            'title':   'Great place!',
            'content': 'Had a wonderful time visiting this place.',
        })
        assert resp.status_code == status.HTTP_201_CREATED

    def test_list_reviews_public(self, api_client, tourist_place):
        resp = api_client.get(f'/api/v1/reviews/?place={tourist_place.pk}')
        assert resp.status_code == status.HTTP_200_OK

    def test_duplicate_review_rejected(self, visitor_client, tourist_place, db):
        visitor_client.post('/api/v1/reviews/', {
            'place': tourist_place.pk, 'rating': 3, 'content': 'OK'
        })
        resp = visitor_client.post('/api/v1/reviews/', {
            'place': tourist_place.pk, 'rating': 5, 'content': 'Great'
        })
        assert resp.status_code == status.HTTP_400_BAD_REQUEST

    def test_invalid_rating(self, visitor_client, tourist_place):
        resp = visitor_client.post('/api/v1/reviews/', {
            'place': tourist_place.pk, 'rating': 6, 'content': 'Test'
        })
        assert resp.status_code == status.HTTP_400_BAD_REQUEST


# ── Travel Plans Tests ────────────────────────────────────────────────────────

class TestTravelPlans:

    def test_create_travel_plan(self, visitor_client):
        resp = visitor_client.post('/api/v1/travel-plans/', {
            'title':      'Goa Trip 2025',
            'start_date': '2025-10-01',
            'end_date':   '2025-10-07',
            'budget':     '30000',
            'currency':   'INR',
            'visibility': 'private',
        })
        assert resp.status_code == status.HTTP_201_CREATED

    def test_list_own_plans(self, visitor_client):
        resp = visitor_client.get('/api/v1/travel-plans/')
        assert resp.status_code == status.HTTP_200_OK

    def test_add_item_to_plan(self, visitor_client, tourist_place):
        create_resp = visitor_client.post('/api/v1/travel-plans/', {
            'title': 'My Trip', 'start_date': '2025-11-01', 'end_date': '2025-11-05',
        })
        plan_id = create_resp.data['id']
        resp = visitor_client.post(f'/api/v1/travel-plans/{plan_id}/add-item/', {
            'place': tourist_place.pk,
            'day':   1,
            'order': 0,
        })
        assert resp.status_code == status.HTTP_201_CREATED

    def test_make_plan_public(self, visitor_client):
        create_resp = visitor_client.post('/api/v1/travel-plans/', {
            'title': 'Shareable Trip', 'start_date': '2025-12-01', 'end_date': '2025-12-03',
        })
        plan_id = create_resp.data['id']
        resp = visitor_client.post(f'/api/v1/travel-plans/{plan_id}/make-public/')
        assert resp.status_code == status.HTTP_200_OK
        assert 'share_token' in resp.data['data']


# ── Analytics Tests ───────────────────────────────────────────────────────────

class TestAnalytics:

    def test_dashboard_admin_only(self, admin_client, visitor_client):
        admin_resp   = admin_client.get('/api/v1/analytics/dashboard/')
        visitor_resp = visitor_client.get('/api/v1/analytics/dashboard/')
        assert admin_resp.status_code == status.HTTP_200_OK
        assert visitor_resp.status_code == status.HTTP_403_FORBIDDEN

    def test_dashboard_kpis(self, admin_client):
        resp = admin_client.get('/api/v1/analytics/dashboard/')
        data = resp.data['data']
        assert 'total_users'    in data
        assert 'total_bookings' in data
        assert 'revenue_total'  in data

    def test_daily_analytics(self, admin_client):
        resp = admin_client.get('/api/v1/analytics/daily/?start=2025-01-01&end=2025-01-31')
        assert resp.status_code == status.HTTP_200_OK

    def test_monthly_analytics(self, admin_client):
        resp = admin_client.get('/api/v1/analytics/monthly/?year=2025')
        assert resp.status_code == status.HTTP_200_OK

    def test_yearly_analytics(self, admin_client):
        resp = admin_client.get('/api/v1/analytics/yearly/')
        assert resp.status_code == status.HTTP_200_OK

    def test_top_places(self, admin_client):
        resp = admin_client.get('/api/v1/analytics/top-places/?metric=bookings&limit=5')
        assert resp.status_code == status.HTTP_200_OK

    def test_export_bookings_csv(self, admin_client):
        resp = admin_client.get('/api/v1/analytics/export/bookings/')
        assert resp.status_code == status.HTTP_200_OK
        assert 'text/csv' in resp.get('Content-Type', '')

    def test_export_revenue_csv(self, admin_client):
        resp = admin_client.get('/api/v1/analytics/export/revenue/')
        assert resp.status_code == status.HTTP_200_OK


# ── Notifications Tests ───────────────────────────────────────────────────────

class TestNotifications:

    def test_list_notifications(self, visitor_client):
        resp = visitor_client.get('/api/v1/notifications/')
        assert resp.status_code == status.HTTP_200_OK

    def test_unread_count(self, visitor_client):
        resp = visitor_client.get('/api/v1/notifications/unread-count/')
        assert resp.status_code == status.HTTP_200_OK
        assert 'unread_count' in resp.data['data']

    def test_admin_broadcast(self, admin_client, visitor_user):
        resp = admin_client.post('/api/v1/notifications/broadcast/', {
            'title':   'System Maintenance',
            'message': 'The system will be down for maintenance.',
            'type':    'system',
            'role':    'visitor',
        })
        assert resp.status_code == status.HTTP_200_OK

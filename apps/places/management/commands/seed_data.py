"""
Management command: python manage.py seed_data
Creates initial categories, a superuser, and sample tourist places.
Safe to run multiple times (uses get_or_create).
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

CATEGORIES = [
    {'name': 'Beach',       'icon': '🏖️',  'sort_order': 1},
    {'name': 'Mountain',    'icon': '⛰️',  'sort_order': 2},
    {'name': 'Museum',      'icon': '🏛️',  'sort_order': 3},
    {'name': 'Temple',      'icon': '🛕',   'sort_order': 4},
    {'name': 'Wildlife',    'icon': '🦁',  'sort_order': 5},
    {'name': 'Waterfall',   'icon': '💦',  'sort_order': 6},
    {'name': 'Hill Station','icon': '🌄',  'sort_order': 7},
    {'name': 'Historical',  'icon': '🏰',  'sort_order': 8},
    {'name': 'City Tour',   'icon': '🏙️',  'sort_order': 9},
    {'name': 'Adventure',   'icon': '🧗',  'sort_order': 10},
]

SAMPLE_PLACES = [
    {
        'name': 'Goa Beach',
        'description': 'Famous for its pristine beaches and vibrant nightlife.',
        'short_desc': 'Sun, sand and sea on India\'s most popular coastline.',
        'category_name': 'Beach',
        'city': 'Goa', 'state': 'Goa', 'country': 'India',
        'address': 'Calangute Beach, North Goa, Goa 403516',
        'latitude': '15.5590', 'longitude': '73.7590',
        'entry_fee': '0.00', 'is_free': True,
        'best_time_to_visit': 'October to March',
        'is_featured': True, 'is_recommended': True,
    },
    {
        'name': 'Taj Mahal',
        'description': 'One of the Seven Wonders of the World, an ivory-white marble mausoleum.',
        'short_desc': 'Iconic Mughal mausoleum and UNESCO World Heritage Site.',
        'category_name': 'Historical',
        'city': 'Agra', 'state': 'Uttar Pradesh', 'country': 'India',
        'address': 'Dharmapuri, Forest Colony, Tajganj, Agra, UP 282001',
        'latitude': '27.1751', 'longitude': '78.0421',
        'entry_fee': '1100.00', 'is_free': False,
        'opening_time': '06:00', 'closing_time': '18:30',
        'open_days': 'Sat-Thu (closed on Friday)',
        'best_time_to_visit': 'October to March',
        'is_featured': True, 'is_recommended': True,
    },
    {
        'name': 'Munnar Hill Station',
        'description': 'Lush green tea estates, misty mountains and cool climate.',
        'short_desc': 'Scenic hill town in the Western Ghats with tea plantations.',
        'category_name': 'Hill Station',
        'city': 'Munnar', 'state': 'Kerala', 'country': 'India',
        'address': 'Munnar, Idukki District, Kerala 685612',
        'latitude': '10.0892', 'longitude': '77.0595',
        'entry_fee': '0.00', 'is_free': True,
        'best_time_to_visit': 'September to May',
        'is_featured': True,
    },
]


class Command(BaseCommand):
    help = 'Seed the database with initial categories, an admin user, and sample places.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.MIGRATE_HEADING('=== Smart Tourism Seed Data ==='))

        # ── Admin user ─────────────────────────────────────────────────────────
        admin, created = User.objects.get_or_create(
            email='admin@smarttourism.com',
            defaults={
                'username':   'admin',
                'first_name': 'Super',
                'last_name':  'Admin',
                'role':       'admin',
                'is_staff':   True,
                'is_superuser': True,
                'is_active':  True,
            }
        )
        if created:
            admin.set_password('Admin@1234')
            admin.save()
            self.stdout.write(self.style.SUCCESS('✔ Admin user created: admin@smarttourism.com / Admin@1234'))
        else:
            self.stdout.write('  Admin user already exists.')

        # ── Sample visitor ─────────────────────────────────────────────────────
        visitor, created = User.objects.get_or_create(
            email='visitor@example.com',
            defaults={
                'username':   'testvisitor',
                'first_name': 'Test',
                'last_name':  'Visitor',
                'role':       'visitor',
                'is_active':  True,
            }
        )
        if created:
            visitor.set_password('Visitor@1234')
            visitor.save()
            from apps.users.models import VisitorProfile
            VisitorProfile.objects.get_or_create(user=visitor)
            self.stdout.write(self.style.SUCCESS('✔ Visitor created: visitor@example.com / Visitor@1234'))

        # ── Categories ─────────────────────────────────────────────────────────
        from apps.places.models import Category
        for cat_data in CATEGORIES:
            cat, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults=cat_data
            )
            mark = '✔' if created else '·'
            self.stdout.write(f'  {mark} Category: {cat.name}')

        # ── Sample places ──────────────────────────────────────────────────────
        from apps.places.models import TouristPlace
        for place_data in SAMPLE_PLACES:
            cat_name = place_data.pop('category_name')
            try:
                category = Category.objects.get(name=cat_name)
            except Category.DoesNotExist:
                continue

            place, created = TouristPlace.objects.get_or_create(
                name=place_data['name'],
                defaults={**place_data, 'category': category, 'created_by': admin, 'status': 'published'}
            )
            mark = '✔' if created else '·'
            self.stdout.write(f'  {mark} Place: {place.name}')

        # ── Cab types ─────────────────────────────────────────────────────────
        from apps.cabs.models import CabType
        cab_types = [
            {'name': 'Hatchback',       'capacity': 4, 'price_per_km': 12, 'base_fare': 50,  'is_ac': True},
            {'name': 'Sedan',           'capacity': 4, 'price_per_km': 15, 'base_fare': 80,  'is_ac': True},
            {'name': 'SUV',             'capacity': 7, 'price_per_km': 20, 'base_fare': 100, 'is_ac': True},
            {'name': 'Tempo Traveller', 'capacity': 12,'price_per_km': 25, 'base_fare': 150, 'is_ac': True},
        ]
        for ct_data in cab_types:
            ct, created = CabType.objects.get_or_create(name=ct_data['name'], defaults=ct_data)
            mark = '✔' if created else '·'
            self.stdout.write(f'  {mark} Cab type: {ct.name}')

        self.stdout.write(self.style.SUCCESS('\n🎉 Seed data complete!'))
        self.stdout.write('\nAPI docs: http://localhost:8000/swagger/')
        self.stdout.write('Admin panel: http://localhost:8000/admin/')
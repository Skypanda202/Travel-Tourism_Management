from django.db import migrations


DEFAULT_CATEGORIES = [
    {
        "name": "Temples",
        "slug": "temples",
        "description": "Sacred and spiritual places for visitors.",
        "icon": "temple",
        "sort_order": 10,
    },
    {
        "name": "Waterfalls",
        "slug": "waterfalls",
        "description": "Waterfalls and scenic water spots.",
        "icon": "waterfall",
        "sort_order": 20,
    },
    {
        "name": "Forts",
        "slug": "forts",
        "description": "Historic forts and defensive monuments.",
        "icon": "fort",
        "sort_order": 30,
    },
    {
        "name": "Heritage Sites",
        "slug": "heritage-sites",
        "description": "Places known for culture, history, and local identity.",
        "icon": "heritage",
        "sort_order": 40,
    },
    {
        "name": "Nature",
        "slug": "nature",
        "description": "Forests, hills, viewpoints, and nature trails.",
        "icon": "nature",
        "sort_order": 50,
    },
    {
        "name": "Wildlife",
        "slug": "wildlife",
        "description": "Sanctuaries and biodiversity destinations.",
        "icon": "wildlife",
        "sort_order": 60,
    },
    {
        "name": "Lakes",
        "slug": "lakes",
        "description": "Lakes, reservoirs, and calm waterfront locations.",
        "icon": "lake",
        "sort_order": 70,
    },
    {
        "name": "Museums",
        "slug": "museums",
        "description": "Museums and educational visitor attractions.",
        "icon": "museum",
        "sort_order": 80,
    },
    {
        "name": "Parks",
        "slug": "parks",
        "description": "Public parks, gardens, and leisure spaces.",
        "icon": "park",
        "sort_order": 90,
    },
]


def seed_categories(apps, schema_editor):
    Category = apps.get_model("places", "Category")

    for category in DEFAULT_CATEGORIES:
        Category.objects.update_or_create(
            slug=category["slug"],
            defaults={
                "name": category["name"],
                "description": category["description"],
                "icon": category["icon"],
                "sort_order": category["sort_order"],
                "is_active": True,
            },
        )


def remove_seeded_categories(apps, schema_editor):
    Category = apps.get_model("places", "Category")
    Category.objects.filter(
        slug__in=[category["slug"] for category in DEFAULT_CATEGORIES]
    ).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("places", "0002_initial"),
    ]

    operations = [
        migrations.RunPython(seed_categories, remove_seeded_categories),
    ]

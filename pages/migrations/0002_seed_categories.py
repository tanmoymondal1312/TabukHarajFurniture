from django.db import migrations

CATEGORIES = [
    {"name": "Majlis & Sofas", "slug": "majlis-sofas", "ordering": 1},
    {"name": "Bedroom Sets", "slug": "bedroom-sets", "ordering": 2},
    {"name": "Dining & Tables", "slug": "dining-tables", "ordering": 3},
    {"name": "Home Appliances", "slug": "home-appliances", "ordering": 4},
    {"name": "Kitchen Furniture", "slug": "kitchen-furniture", "ordering": 5},
    {"name": "Other Furniture", "slug": "other-furniture", "ordering": 6},
]


def seed_categories(apps, schema_editor):
    Category = apps.get_model("pages", "Category")
    for item in CATEGORIES:
        Category.objects.get_or_create(
            slug=item["slug"],
            defaults={"name": item["name"], "ordering": item["ordering"]},
        )


def remove_categories(apps, schema_editor):
    Category = apps.get_model("pages", "Category")
    Category.objects.filter(slug__in=[c["slug"] for c in CATEGORIES]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("pages", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed_categories, remove_categories),
    ]

from django.db import migrations

# New categories taken from the SEO tags (knowsAbout / description):
# Air Conditioners, Refrigerators, Washing Machines, Mattresses,
# plus two common showroom groups: Office Furniture, Curtains & Carpets.
NEW_CATEGORIES = [
    {"name": "Air Conditioners", "ar_name": "مكيفات", "slug": "air-conditioners", "ordering": 7},
    {"name": "Refrigerators & Freezers", "ar_name": "ثلاجات وفريزر", "slug": "refrigerators-freezers", "ordering": 8},
    {"name": "Washing Machines", "ar_name": "غسالات", "slug": "washing-machines", "ordering": 9},
    {"name": "Mattresses & Beds", "ar_name": "مراتب وأسرّة", "slug": "mattresses-beds", "ordering": 10},
    {"name": "Office Furniture", "ar_name": "أثاث مكتبي", "slug": "office-furniture", "ordering": 11},
    {"name": "Curtains & Carpets", "ar_name": "ستائر وسجاد", "slug": "curtains-carpets", "ordering": 12},
]

# Arabic names for the 6 categories that already exist
EXISTING_AR_NAMES = {
    "majlis-sofas": "صالونات ومجالس",
    "bedroom-sets": "غرف نوم",
    "dining-tables": "غرف طعام وطاولات",
    "home-appliances": "أجهزة منزلية",
    "kitchen-furniture": "أثاث مطبخ",
    "other-furniture": "أثاث متنوع",
}

PLACEHOLDER_IMAGE = "categories/placeholder.webp"


def seed_more_categories(apps, schema_editor):
    Category = apps.get_model("pages", "Category")
    for item in NEW_CATEGORIES:
        Category.objects.get_or_create(
            slug=item["slug"],
            defaults={
                "name": item["name"],
                "ar_name": item["ar_name"],
                "ordering": item["ordering"],
            },
        )
    for slug, ar_name in EXISTING_AR_NAMES.items():
        Category.objects.filter(slug=slug).update(ar_name=ar_name)
    # Every category uses the placeholder image until real photos are uploaded
    Category.objects.all().update(image=PLACEHOLDER_IMAGE)


def remove_more_categories(apps, schema_editor):
    Category = apps.get_model("pages", "Category")
    Category.objects.filter(slug__in=[c["slug"] for c in NEW_CATEGORIES]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("pages", "0002_seed_categories"),
    ]

    operations = [
        migrations.RunPython(seed_more_categories, remove_more_categories),
    ]

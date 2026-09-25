from django.db import migrations

# Majlis & Sofas, Bedroom Sets and Dining & Tables move to the end.
NEW_ORDER = {
    "home-appliances": 1,
    "kitchen-furniture": 2,
    "other-furniture": 3,
    "air-conditioners": 4,
    "refrigerators-freezers": 5,
    "washing-machines": 6,
    "mattresses-beds": 7,
    "office-furniture": 8,
    "curtains-carpets": 9,
    "majlis-sofas": 10,
    "bedroom-sets": 11,
    "dining-tables": 12,
}

OLD_ORDER = {
    "majlis-sofas": 1,
    "bedroom-sets": 2,
    "dining-tables": 3,
    "home-appliances": 4,
    "kitchen-furniture": 5,
    "other-furniture": 6,
    "air-conditioners": 7,
    "refrigerators-freezers": 8,
    "washing-machines": 9,
    "mattresses-beds": 10,
    "office-furniture": 11,
    "curtains-carpets": 12,
}


def reorder(apps, schema_editor):
    Category = apps.get_model("pages", "Category")
    for slug, ordering in NEW_ORDER.items():
        Category.objects.filter(slug=slug).update(ordering=ordering)


def undo_reorder(apps, schema_editor):
    Category = apps.get_model("pages", "Category")
    for slug, ordering in OLD_ORDER.items():
        Category.objects.filter(slug=slug).update(ordering=ordering)


class Migration(migrations.Migration):

    dependencies = [
        ("pages", "0003_seed_more_categories"),
    ]

    operations = [
        migrations.RunPython(reorder, undo_reorder),
    ]

from django.shortcuts import render

CATEGORIES = [
    {"name": "Majlis & Sofas", "count": "120+ items", "image": "category-majlis-sofas.webp"},
    {"name": "Bedroom Sets", "count": "98+ items", "image": "category-bedroom-sets.webp"},
    {"name": "Dining & Tables", "count": "76+ items", "image": "category-dining-tables.webp"},
    {"name": "Home Appliances", "count": "210+ items", "image": "category-home-appliances.webp"},
    {"name": "Kitchen Furniture", "count": "64+ items", "image": "category-kitchen-furniture.webp"},
    {"name": "Other Furniture", "count": "45+ items", "image": "category-other-furniture.webp"},
]

LISTINGS = [
    {"title": "مجلس عربي فاخر", "price": "SAR 2,500", "image": "placeholder.webp"},
    {"title": "مكيف سبليت 18000 وحدة", "price": "SAR 1,800", "image": "placeholder.webp"},
    {"title": "ثلاجة سامسونج", "price": "SAR 2,200", "image": "placeholder.webp"},
    {"title": "غرفة نوم كاملة", "price": "SAR 3,500", "image": "placeholder.webp"},
]


def home(request):
    return render(request, "pages/home.html", {
        "categories": CATEGORIES,
        "listings": LISTINGS,
        "q": request.GET.get("q", ""),
    })

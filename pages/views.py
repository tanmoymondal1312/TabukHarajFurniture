from django.shortcuts import render

from django.conf import settings

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
    # Set SEO context for the homepage
    request.page_title = "حراج تبوك للأثاث المستعمل | معرض فعلي • ضمان 30 يوم • توصيل مجاني"
    request.page_description = "حراج تبوك للأثاث المستعمل — معرض فعلي في تبوك، ضمان 30 يوم وتوصيل مجاني. أثاث وأجهزة مستعملة موثوقة بأفضل الأسعار: صالونات، غرف نوم، مكيفات والمزيد."
    request.page_image = "https://tabukharajfurniture.com/static/images/clean-modern-room-with-beautifull-furniture.webp"

    return render(request, "pages/home.html", {
        "categories": CATEGORIES,
        "listings": LISTINGS,
        "q": request.GET.get("q", ""),
    })


def faq(request):
    request.page_title = "الأسئلة الشائعة | حراج تبوك للأثاث"
    request.page_description = "إجابات على الأسئلة الشائعة حول حراج تبوك للأثاث: الموقع، الضمان، التوصيل، الشراء، البيع، طرق الدفع، وأنواع الأجهزة المتوفرة."
    request.page_image = "https://tabukharajfurniture.com/static/images/clean-modern-room-with-beautifull-furniture.webp"

    return render(request, "pages/faq.html", {})

from django.shortcuts import render

from .models import Category, Product


def home(request):
    # Set SEO context for the homepage
    request.page_title = "حراج تبوك للأثاث المستعمل | معرض فعلي • ضمان 30 يوم • توصيل مجاني"
    request.page_description = "حراج تبوك للأثاث المستعمل — معرض فعلي في تبوك، ضمان 30 يوم وتوصيل مجاني. أثاث وأجهزة مستعملة موثوقة بأفضل الأسعار: صالونات، غرف نوم، مكيفات والمزيد."
    request.page_image = "https://tabukharajfurniture.com/static/images/clean-modern-room-with-beautifull-furniture.webp"

    listings = (
        Product.objects.filter(is_active=True, status=Product.STATUS_AVAILABLE)
        .order_by("-is_featured", "-created_at")[:8]
    )
    return render(request, "pages/home.html", {
        "categories": Category.objects.filter(is_active=True),
        "listings": listings,
        "q": request.GET.get("q", ""),
    })


def faq(request):
    request.page_title = "الأسئلة الشائعة | حراج تبوك للأثاث"
    request.page_description = "إجابات على الأسئلة الشائعة حول حراج تبوك للأثاث: الموقع، الضمان، التوصيل، الشراء، البيع، طرق الدفع، وأنواع الأجهزة المتوفرة."
    request.page_image = "https://tabukharajfurniture.com/static/images/clean-modern-room-with-beautifull-furniture.webp"

    return render(request, "pages/faq.html", {})

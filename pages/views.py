from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from .models import Category, Product

CANONICAL = "https://tabukharajfurniture.com"


def home(request):
    # Set SEO context for the homepage
    request.page_title = "حراج تبوك للأثاث المستعمل | معرض فعلي • ضمان 30 يوم • توصيل مجاني"
    request.page_description = "حراج تبوك للأثاث المستعمل — معرض فعلي في تبوك، ضمان 30 يوم وتوصيل مجاني. أثاث وأجهزة مستعملة موثوقة بأفضل الأسعار: صالونات، غرف نوم، مكيفات والمزيد."
    request.page_image = "https://tabukharajfurniture.com/static/images/clean-modern-room-with-beautifull-furniture.webp"

    listings = (
        Product.objects.filter(is_active=True, status=Product.STATUS_AVAILABLE)
        .order_by("-is_featured", "-created_at")
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


def products(request):
    request.page_title = "كل المنتجات | حراج تبوك للأثاث المستعمل"
    request.page_description = "تصفح جميع المنتجات في حراج تبوك للأثاث المستعمل: أثاث، مكيفات، ثلاجات، غسالات وأكثر. كل قطعة مختبرة بضمان 30 يوم وتوصيل مجاني في تبوك."
    request.page_image = "https://tabukharajfurniture.com/static/images/clean-modern-room-with-beautifull-furniture.webp"

    categories = Category.objects.filter(is_active=True)

    active_category = None
    cat_slug = request.GET.get("cat", "")
    if cat_slug:
        active_category = get_object_or_404(Category, slug=cat_slug, is_active=True)

    items = Product.objects.filter(
        is_active=True, status=Product.STATUS_AVAILABLE
    )
    if active_category:
        items = items.filter(category=active_category)
    items = items.order_by("-is_featured", "-created_at")

    total = Product.objects.filter(
        is_active=True, status=Product.STATUS_AVAILABLE
    ).count()

    return render(request, "pages/products.html", {
        "categories": categories,
        "active_category": active_category,
        "products": items,
        "showing_count": items.count(),
        "total_count": total,
    })


def product_detail(request, slug):
    product = get_object_or_404(
        Product.objects.select_related("category"), slug=slug, is_active=True
    )

    description = (product.description or "").strip()
    if not description:
        description = f"{product.title} — متجر حراج تبوك للأثاث المستعمل. تواصل معنا للسؤال عن هذه القطعة."

    request.page_title = f"{product.title} | حراج تبوك للأثاث المستعمل"
    request.page_description = description[:155]
    if product.image:
        request.page_image = CANONICAL + product.image.url

    related = list(
        Product.objects.filter(
            is_active=True,
            status=Product.STATUS_AVAILABLE,
            category_id=product.category_id,
        )
        .exclude(pk=product.pk)[:4]
    )
    if len(related) < 4:
        related += list(
            Product.objects.filter(
                is_active=True, status=Product.STATUS_AVAILABLE
            )
            .exclude(pk=product.pk)
            .exclude(pk__in=[p.pk for p in related])[: 4 - len(related)]
        )

    product_url = CANONICAL + product.get_absolute_url()
    if product.image:
        product_image_url = CANONICAL + product.image.url
    else:
        product_image_url = CANONICAL + "/static/images/placeholder.webp"

    wa_text = (
        "السلام عليكم، أريد الاستفسار عن هذا المنتج:\n"
        f"{product.title} — {product.price_display}\n{product_url}"
    )

    discount = 0
    if product.has_discount:
        discount = round(
            float((product.old_price - product.price) / product.old_price) * 100
        )

    return render(request, "pages/product.html", {
        "product": product,
        "related": related,
        "description": description,
        "listed_date": timezone.localtime(product.created_at).strftime("%d %b %Y"),
        "product_url": product_url,
        "product_image_url": product_image_url,
        "wa_text": wa_text,
        "discount": discount,
    })

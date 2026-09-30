import re

from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone

from .models import Category, ContactMessage, Product

CANONICAL = "https://tabukharajfurniture.com"
OG_COVER = CANONICAL + "/static/images/og-cover.jpg"


def home(request):
    # Set SEO context for the homepage
    request.page_title = "حراج تبوك للأثاث المستعمل | معرض فعلي • ضمان 30 يوم • توصيل مجاني"
    request.page_description = "حراج تبوك للأثاث المستعمل — معرض فعلي في تبوك، ضمان 30 يوم وتوصيل مجاني. أثاث وأجهزة مستعملة موثوقة بأفضل الأسعار: صالونات، غرف نوم، مكيفات والمزيد."
    request.page_image = OG_COVER

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
    request.page_title = "الأسئلة الشائعة | حراج تبوك للأثاث المستعمل"
    request.page_description = "أسئلة وأجوبة كاملة عن حراج تبوك للأثاث المستعمل في تبوك: موقع المعرض وساعات العمل، ضمان 30 يوم، التوصيل المجاني، طرق الدفع، تجربة الأجهزة قبل الشراء، والبيع والشراء."
    request.page_image = OG_COVER

    return render(request, "pages/faq.html", {})


def about(request):
    request.page_title = "من نحن | حراج تبوك للأثاث المستعمل"
    request.page_description = "قصة حراج تبوك للأثاث: من معرض فارغ نهاية 2023 إلى ثقة 800+ عائلة. كيف نعمل، من أين نجلب الأثاث، خدماتنا الكاملة، ضمان 30 يوم خدمة، وفريقنا."
    request.page_image = OG_COVER

    return render(request, "pages/about.html", {})


def contact(request):
    request.page_title = "اتصل بنا | حراج تبوك للأثاث المستعمل"
    request.page_description = (
        "تواصل مع حراج تبوك للأثاث المستعمل: اتصال مباشر 0582328389، واتساب، "
        "بريد إلكتروني، ونموذج رسالة يصلك مباشرة. معرضنا في المنشية القديمة، تبوك — "
        "السبت–الخميس 9:00–22:00."
    )
    request.page_image = OG_COVER

    errors = {}
    form = {"name": "", "phone": "", "subject": "", "body": ""}

    if request.method == "POST":
        if request.POST.get("website"):
            # Honeypot: bots fill the hidden field — pretend success.
            return redirect(reverse("pages:contact") + "?sent=1")

        for key in form:
            form[key] = (request.POST.get(key) or "").strip()[:2000]

        if len(form["name"]) < 2:
            errors["name"] = "اكتب اسمك من فضلك."
        if len(form["body"]) < 5:
            errors["body"] = "اكتب رسالتك (5 أحرف على الأقل)."
        if form["phone"] and not re.fullmatch(r"[0-9+\s\-]{8,20}", form["phone"]):
            errors["phone"] = "رقم الجوال غير صحيح. مثال: 0582328389"

        if not errors:
            ContactMessage.objects.create(
                name=form["name"][:120],
                phone=form["phone"][:30],
                subject=form["subject"][:60],
                body=form["body"][:2000],
            )
            return redirect(reverse("pages:contact") + "?sent=1")

    return render(request, "pages/contact.html", {
        "sent": request.GET.get("sent") == "1",
        "errors": errors,
        "form": form,
        "has_errors": bool(errors),
    })


def products(request):
    request.page_title = "كل المنتجات | حراج تبوك للأثاث المستعمل"
    request.page_description = "تصفح جميع المنتجات في حراج تبوك للأثاث المستعمل: أثاث، مكيفات، ثلاجات، غسالات وأكثر. كل قطعة مختبرة بضمان 30 يوم وتوصيل مجاني في تبوك."
    request.page_image = OG_COVER

    categories = Category.objects.filter(is_active=True)

    active_category = None
    cat_slug = request.GET.get("cat", "")
    if cat_slug:
        active_category = get_object_or_404(Category, slug=cat_slug, is_active=True)
        if active_category.image:
            request.page_title = (
                f"{active_category.ar_name or active_category.name} | حراج تبوك للأثاث"
            )
            request.page_image = CANONICAL + active_category.image.url

    items = Product.objects.filter(
        is_active=True, status=Product.STATUS_AVAILABLE
    )
    if active_category:
        items = items.filter(category=active_category)

    q = request.GET.get("q", "").strip()[:60]
    if q:
        items = items.filter(
            Q(title__icontains=q)
            | Q(description__icontains=q)
            | Q(category__name__icontains=q)
            | Q(category__ar_name__icontains=q)
        )
    items = items.order_by("-is_featured", "-created_at")

    total = Product.objects.filter(
        is_active=True, status=Product.STATUS_AVAILABLE
    ).count()

    return render(request, "pages/products.html", {
        "categories": categories,
        "active_category": active_category,
        "products": items,
        "q": q,
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
    else:
        request.page_image = OG_COVER

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

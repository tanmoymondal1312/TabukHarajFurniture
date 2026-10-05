import re

from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import get_language

from pages.templatetags.site_lang import translate

from .models import Category, ContactMessage, Product

CANONICAL = "https://tabukharajfurniture.com"
OG_COVER = CANONICAL + "/static/images/og-cover.jpg"

_AR_MONTHS = {
    1: "يناير", 2: "فبراير", 3: "مارس", 4: "أبريل", 5: "مايو", 6: "يونيو",
    7: "يوليو", 8: "أغسطس", 9: "سبتمبر", 10: "أكتوبر", 11: "نوفمبر", 12: "ديسمبر",
}


def _listed_date(value):
    d = timezone.localtime(value)
    if get_language() == "ar":
        return f"{d.day:02d} {_AR_MONTHS[d.month]} {d.year}"
    return d.strftime("%d %b %Y")


def _is_en():
    return (get_language() or "ar").split("-")[0].lower() == "en"


def _set_seo(request, *, ar_title, en_title, ar_desc, en_desc, image=None):
    """Set the page <title>, meta description and OG image for the
    active language, so Arabic and English pages each get their own
    search-engine snippet."""
    if _is_en():
        request.page_title = en_title
        request.page_description = en_desc
    else:
        request.page_title = ar_title
        request.page_description = ar_desc
    request.page_image = image or OG_COVER


def home(request):
    # Set SEO context for the homepage
    _set_seo(
        request,
        ar_title="حراج تبوك للأثاث المستعمل | معرض فعلي • ضمان 30 يوم • توصيل مجاني",
        en_title="Used Furniture & Appliances in Tabuk | 30-Day Warranty • Free Delivery",
        ar_desc="حراج تبوك للأثاث المستعمل — معرض فعلي في تبوك، ضمان 30 يوم وتوصيل مجاني. أثاث وأجهزة مستعملة موثوقة بأفضل الأسعار: صالونات، غرف نوم، مكيفات والمزيد.",
        en_desc="Physical showroom in Tabuk for tested used furniture and appliances: sofas, bedroom sets, ACs, fridges and washing machines. 30-day warranty, free delivery across Tabuk, instant cash for sellers.",
    )

    listings = (
        Product.objects.filter(
            is_active=True,
            status=Product.STATUS_AVAILABLE,
            category__is_active=True,
        )
        .order_by("-is_featured", "-created_at")
    )
    return render(request, "pages/home.html", {
        "categories": Category.objects.filter(is_active=True),
        "listings": listings,
        "q": request.GET.get("q", ""),
    })


def faq(request):
    _set_seo(
        request,
        ar_title="الأسئلة الشائعة | حراج تبوك للأثاث المستعمل",
        en_title="Frequently Asked Questions | Tabuk Haraj Furniture",
        ar_desc="أسئلة وأجوبة كاملة عن حراج تبوك للأثاث المستعمل في تبوك: موقع المعرض وساعات العمل، ضمان 30 يوم، التوصيل المجاني، طرق الدفع، تجربة الأجهزة قبل الشراء، والبيع والشراء.",
        en_desc="Answers about Tabuk Haraj Furniture: showroom location and hours, 30-day warranty, free delivery, payment methods, testing items before buying, and selling your used furniture.",
    )

    return render(request, "pages/faq.html", {})


def about(request):
    _set_seo(
        request,
        ar_title="من نحن | شراء وبيع الأثاث والمكيفات والثلاجات المستعملة في تبوك",
        en_title="About Us | Used Furniture & Appliances in Tabuk",
        ar_desc=(
            "حراج تبوك للأثاث: نشتري ونبيع الأثاث والمكيفات والثلاجات والغسالات المستعملة في تبوك. "
            "قصة معرضنا، فحص القطع قبل البيع، ضمان 30 يوم، توصيل مجاني، وخدماتنا للمنازل والشركات."
        ),
        en_desc=(
            "Tabuk Haraj Furniture buys and sells used furniture, ACs, fridges and washing "
            "machines in Tabuk. Our story, how we check every item, 30-day warranty, free "
            "delivery and our services for homes and businesses."
        ),
    )

    return render(request, "pages/about.html", {
        "categories": Category.objects.filter(is_active=True),
    })


def contact(request):
    _set_seo(
        request,
        ar_title="اتصل بنا | حراج تبوك للأثاث المستعمل",
        en_title="Contact Us | Tabuk Haraj Furniture",
        ar_desc=(
            "تواصل مع حراج تبوك للأثاث المستعمل: اتصال مباشر 0582328389، واتساب، "
            "بريد إلكتروني، ونموذج رسالة يصلك مباشرة. معرضنا في المنشية القديمة، تبوك — "
            "السبت–الخميس 9:00–22:00."
        ),
        en_desc=(
            "Contact Tabuk Haraj Furniture: call 0582328389, WhatsApp, email, or send a "
            "message that reaches us directly. Showroom in Al Munshiyah Al Qadimah, Tabuk — "
            "Sat-Thu 9:00-22:00."
        ),
    )

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
    _set_seo(
        request,
        ar_title="كل المنتجات | حراج تبوك للأثاث المستعمل",
        en_title="All Products | Used Furniture & Appliances in Tabuk",
        ar_desc="تصفح جميع المنتجات في حراج تبوك للأثاث المستعمل: أثاث، مكيفات، ثلاجات، غسالات وأكثر. كل قطعة مختبرة بضمان 30 يوم وتوصيل مجاني في تبوك.",
        en_desc="Browse all used furniture and appliances in Tabuk: sofas, bedroom sets, ACs, fridges, washers and more. Every item tested, 30-day warranty, free delivery in Tabuk.",
    )

    categories = Category.objects.filter(is_active=True)

    active_category = None
    cat_slug = request.GET.get("cat", "")
    if cat_slug:
        active_category = get_object_or_404(Category, slug=cat_slug, is_active=True)
        name = active_category.display_name
        if _is_en():
            request.page_title = f"{name} | Tabuk Haraj Furniture"
            request.page_description = (
                f"Browse used {name.lower()} in Tabuk — tested items with "
                "30-day warranty and free delivery."
            )
        else:
            request.page_title = f"{name} | حراج تبوك للأثاث"
            request.page_description = (
                f"{name} — مستعمل مختبر بضمان 30 يوم وتوصيل مجاني في تبوك. "
                "تصفّح كل القطع المتاحة الآن."
            )
        custom_desc = active_category.display_description.strip()
        if custom_desc:
            # Admin-written text wins for both the meta description
            # and the short intro shown under the category title.
            request.page_description = custom_desc[:155]
        if active_category.image:
            request.page_image = CANONICAL + active_category.image.url

    items = Product.objects.filter(
        is_active=True,
        status=Product.STATUS_AVAILABLE,
        category__is_active=True,
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
        is_active=True,
        status=Product.STATUS_AVAILABLE,
        category__is_active=True,
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
        Product.objects.select_related("category"),
        slug=slug,
        is_active=True,
        category__is_active=True,
    )

    description = (product.description or "").strip()
    if not description:
        description = f"{product.title} — متجر حراج تبوك للأثاث المستعمل. تواصل معنا للسؤال عن هذه القطعة."

    if _is_en():
        request.page_title = f"{product.title} | Tabuk Haraj Furniture"
        request.page_description = (
            f"{product.title} — tested used item at Tabuk Haraj Furniture in "
            "Tabuk. 30-day warranty, free delivery. Call 0582328389."
        )[:155]
    else:
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
                is_active=True,
                status=Product.STATUS_AVAILABLE,
                category__is_active=True,
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
        "listed_date": _listed_date(product.created_at),
        "product_url": product_url,
        "product_image_url": product_image_url,
        "wa_text": wa_text,
        "discount": discount,
    })


def product_order(request, slug):
    """Accept a "Direct Order" request from the product page.

    Saves it as a ContactMessage with kind="order", so it shows up in
    the dashboard inbox like any other message, with an order badge.
    JSON is returned for the Ajax form; a plain redirect for no-JS.
    """
    product = get_object_or_404(
        Product.objects.select_related("category"),
        slug=slug,
        is_active=True,
        category__is_active=True,
    )
    if request.method != "POST":
        return redirect(product.get_absolute_url())

    wants_json = request.headers.get("X-Requested-With") == "XMLHttpRequest"

    def success():
        if wants_json:
            return JsonResponse({"ok": True, "errors": {}})
        return redirect(product.get_absolute_url() + "?ordered=1")

    if request.POST.get("website"):
        # Honeypot: bots fill the hidden field — pretend success.
        return success()

    data = {
        "name": (request.POST.get("name") or "").strip()[:120],
        "phone": (request.POST.get("phone") or "").strip()[:30],
        "address": (request.POST.get("address") or "").strip()[:200],
        "notes": (request.POST.get("notes") or "").strip()[:1000],
    }

    errors = {}
    if len(data["name"]) < 2:
        errors["name"] = translate("Please write your name.")
    if not data["phone"]:
        errors["phone"] = translate("Please write your phone number.")
    elif not re.fullmatch(r"[0-9+\s\-]{8,20}", data["phone"]):
        errors["phone"] = translate(
            "Phone number is not valid. Example: 0582328389"
        )
    if len(data["address"]) < 3:
        errors["address"] = translate("Please write your delivery address.")

    if errors:
        if wants_json:
            return JsonResponse({"ok": False, "errors": errors})
        # No-JS: re-render the product page with the modal open.
        request.order_errors = errors
        request.order_values = data
        return product_detail(request, slug)

    body_lines = [
        f"Product: {product.title}",
        f"Price: {product.price_display}",
        f"URL: {CANONICAL + product.get_absolute_url()}",
        "",
        f"Name: {data['name']}",
        f"Phone: {data['phone']}",
        f"Address: {data['address']}",
    ]
    if data["notes"]:
        body_lines.append(f"Notes: {data['notes']}")

    ContactMessage.objects.create(
        kind="order",
        name=data["name"],
        phone=data["phone"],
        subject=product.title[:60],
        body="\n".join(body_lines)[:2000],
    )
    return success()

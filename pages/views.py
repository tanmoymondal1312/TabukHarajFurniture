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


# ---- /sell/ page: we buy used furniture from people in Tabuk ----

_SELL = {
    "seo": {
        "ar_title": "نشتري الأثاث المستعمل في تبوك | عرض سعر فوري",
        "en_title": "We Buy Used Furniture in Tabuk | Instant Cash Offer",
        "ar_desc": (
            "نشتري الأثاث والأجهزة المستعملة في تبوك: كنب، غرف نوم، مكيفات، "
            "ثلاجات، غسالات. أرسل صور القطعة واحصل على عرض سعر فوري — استلام "
            "مجاني داخل تبوك ودفع كاش في نفس الزيارة."
        ),
        "en_desc": (
            "We buy used furniture and appliances in Tabuk: sofas, bedroom sets, "
            "ACs, fridges, washers. Send photos for an instant offer — free "
            "pickup across Tabuk and cash paid on the spot."
        ),
    },
    "ar": {
        "eyebrow": "نشتري منك",
        "title": "نشتري أثاثك المستعمل في تبوك",
        "lead": (
            "تبي تبيع كنب، غرفة نوم، مكيف، ثلاجة أو أي جهاز مستعمل؟ أرسل صور "
            "القطعة على واتساب واحصل على عرض سعر فوري — استلام مجاني من أي حي "
            "في تبوك ودفع كاش في نفس الزيارة."
        ),
        "steps_title": "كيف نعمل",
        "steps": [
            ("أرسل صور القطعة",
             "راسلنا على واتساب 058 232 8389 مع صور القطعة وحالتها، أو املأ "
             "النموذج في هذه الصفحة."),
            ("احصل على عرض سعر",
             "نقيّم القطعة بسرعة ونرسل لك سعراً عادلاً حسب الحالة والعمر والماركة."),
            ("نستلم وندفع كاش",
             "بعد موافقتك نستلم القطعة من موقعك مجاناً داخل تبوك وندفع لك كاش "
             "في نفس الزيارة."),
        ],
        "buy_title": "ماذا نشتري؟",
        "buy_items": [
            "كنب ومجالس", "غرف نوم", "خزائن ودواليب", "طاولات وكراسي",
            "مطابخ", "مكيفات", "ثلاجات وفريزر", "غسالات", "أفران ومايكروويف",
        ],
        "form_title": "اطلب عرض سعر",
        "form_sub": (
            "اكتب تفاصيل القطع وسنتواصل معك بسرعة — عادة خلال ساعة في أوقات العمل."
        ),
        "schema_name": "نشتري الأثاث المستعمل في تبوك",
        "schema_desc": (
            "خدمة شراء الأثاث والأجهزة المستعملة في تبوك: عرض سعر فوري، "
            "استلام مجاني، ودفع كاش."
        ),
    },
    "en": {
        "eyebrow": "We buy from you",
        "title": "We Buy Your Used Furniture in Tabuk",
        "lead": (
            "Want to sell a sofa, bedroom set, AC, fridge or any used item? Send "
            "us photos on WhatsApp for an instant offer — free pickup from any "
            "district in Tabuk and cash paid on the spot."
        ),
        "steps_title": "How it works",
        "steps": [
            ("Send us photos",
             "Message us on WhatsApp 058 232 8389 with photos of the item and "
             "its condition, or fill in the form on this page."),
            ("Get a price offer",
             "We check the item quickly and send you a fair price based on "
             "condition, age and brand."),
            ("We pick up, you get cash",
             "After you agree, we collect the item from your location for free "
             "anywhere in Tabuk and pay you cash on the spot."),
        ],
        "buy_title": "What do we buy?",
        "buy_items": [
            "Sofas & majlis sets", "Bedroom sets", "Wardrobes", "Tables & chairs",
            "Kitchen sets", "Air conditioners", "Fridges & freezers",
            "Washing machines", "Ovens & microwaves",
        ],
        "form_title": "Request a price offer",
        "form_sub": (
            "Tell us about your items and we will get back to you fast — usually "
            "within an hour during opening hours."
        ),
        "schema_name": "We Buy Used Furniture in Tabuk",
        "schema_desc": (
            "We buy used furniture and appliances in Tabuk: instant price offer, "
            "free pickup, and cash payment."
        ),
    },
}


def sell(request):
    """Lead-capture page for people who want to sell used furniture."""
    _set_seo(request, **_SELL["seo"])
    body = _SELL["en"] if _is_en() else _SELL["ar"]
    sell_url = CANONICAL + reverse("pages:sell")

    errors = {}
    form = {"name": "", "phone": "", "items": ""}

    if request.method == "POST":
        if request.POST.get("website"):
            # Honeypot: bots fill the hidden field — pretend success.
            return redirect(reverse("pages:sell") + "?sent=1")

        for key in form:
            form[key] = (request.POST.get(key) or "").strip()[:2000]

        if len(form["name"]) < 2:
            errors["name"] = (
                "Please write your name." if _is_en() else "اكتب اسمك من فضلك."
            )
        if not form["phone"]:
            errors["phone"] = (
                "Please write your phone number." if _is_en() else "اكتب رقم جوالك من فضلك."
            )
        elif not re.fullmatch(r"[0-9+\s\-]{8,20}", form["phone"]):
            errors["phone"] = (
                "Invalid phone number. Example: 0582328389" if _is_en()
                else "رقم الجوال غير صحيح. مثال: 0582328389"
            )
        if len(form["items"]) < 5:
            errors["items"] = (
                "Tell us what you want to sell (5 characters minimum)."
                if _is_en() else "اكتب ما تريد بيعه (5 أحرف على الأقل)."
            )

        if not errors:
            # Shows in the dashboard Messages tab as a normal message.
            ContactMessage.objects.create(
                name=form["name"][:120],
                phone=form["phone"][:30],
                subject="Sell request",
                body=form["items"][:2000],
            )
            return redirect(reverse("pages:sell") + "?sent=1")

    return render(request, "pages/sell.html", {
        "sent": request.GET.get("sent") == "1",
        "errors": errors,
        "form": form,
        "has_errors": bool(errors),
        "sell_url": sell_url,
        "sell_eyebrow": body["eyebrow"],
        "sell_title": body["title"],
        "sell_lead": body["lead"],
        "sell_steps_title": body["steps_title"],
        "sell_steps": [{"h": h, "p": p} for h, p in body["steps"]],
        "sell_buy_title": body["buy_title"],
        "sell_buy_items": body["buy_items"],
        "sell_form_title": body["form_title"],
        "sell_form_sub": body["form_sub"],
        "sell_schema_name": body["schema_name"],
        "sell_schema_desc": body["schema_desc"],
    })


# ---- Static policy pages: /shipping/ /returns/ /privacy/ /terms/ ----
# Content lives here (not in translations.py) because these are long
# page bodies, not small UI labels. Facts come from the FAQ page, so
# every promise on the site stays the same.

_POLICIES = {
    "shipping": {
        "seo": {
            "ar_title": "التوصيل والاستلام | حراج تبوك للأثاث المستعمل",
            "en_title": "Delivery & Pickup | Tabuk Haraj Furniture",
            "ar_desc": (
                "توصيل مجاني لجميع أحياء تبوك عادةً في نفس اليوم أو اليوم التالي، "
                "واستلام من المعرض في المنشية القديمة، طريق معاوية. لا يوجد توصيل خارج تبوك."
            ),
            "en_desc": (
                "Free delivery across all Tabuk districts, usually the same day or the "
                "next day. Pick up from our showroom in Al Munshiyah Al Qadimah. No "
                "delivery outside Tabuk city."
            ),
        },
        "ar": {
            "title": "التوصيل والاستلام",
            "sections": [
                ("التوصيل مجاني داخل تبوك",
                 "التوصيل مجاني لجميع أحياء تبوك: النخيل، الحصاة، المروج، الشروق، الخالدية، "
                 "العزيزية، البوادي، الروضة، المنشية القديمة وغيرها. معظم الطلبات تصل في نفس "
                 "اليوم أو اليوم التالي حسب الوقت."),
                ("التوصيل داخل مدينة تبوك فقط",
                 "نوصل ونستلم داخل مدينة تبوك فقط. إذا كنت خارج تبوك، يمكنك الاستلام من "
                 "المعرض مباشرة."),
                ("الاستلام من المعرض",
                 "معرضنا في المنشية القديمة، طريق معاوية، تبوك 47914، السعودية. ساعات العمل: "
                 "السبت–الخميس 9:00 صباحاً حتى 10:00 مساءً، والجمعة من 4:00 مساءً حتى 10:00 مساءً."),
                ("ساعدنا في التوصيل السريع",
                 "عند الطلب، اكتب الحي والشارع والدور بوضوح. إذا كان لديك وقت مفضل، أخبرنا على "
                 "واتساب 058 232 8389."),
            ],
        },
        "en": {
            "title": "Delivery & Pickup",
            "sections": [
                ("Free delivery in Tabuk",
                 "Delivery is free to all districts of Tabuk: Al Nakheel, Al Hasah, Al Muruj, "
                 "Al Shuruq, Al Khalidiyah, Al Aziziyah, Al Bawadi, Al Rawdah, Al Munshiyah Al "
                 "Qadimah and more. Most orders arrive the same day or the next day."),
                ("Inside Tabuk city only",
                 "We deliver and pick up inside Tabuk city only. If you are outside Tabuk, you "
                 "are welcome to pick up your item from the showroom."),
                ("Pick up from the showroom",
                 "Our showroom is in Al Munshiyah Al Qadimah, Muawiyah Road, Tabuk 47914, Saudi "
                 "Arabia. Open Saturday to Thursday 9:00-22:00 and Friday 16:00-22:00."),
                ("Help us deliver faster",
                 "When you place an order, write your district, street and floor clearly. If you "
                 "have a preferred time, tell us on WhatsApp 058 232 8389."),
            ],
        },
    },
    "returns": {
        "seo": {
            "ar_title": "الاسترجاع والاستبدال | حراج تبوك للأثاث المستعمل",
            "en_title": "Returns & Exchanges | Tabuk Haraj Furniture",
            "ar_desc": (
                "ضمان استبدال 30 يوم على كل قطعة بدون استرداد نقدي — كيف تطلب الاستبدال "
                "وما الذي يغطيه الضمان في حراج تبوك للأثاث."
            ),
            "en_desc": (
                "30-day exchange warranty on every item, no cash refund. How to request an "
                "exchange and what the warranty covers at Tabuk Haraj Furniture."
            ),
        },
        "ar": {
            "title": "الاسترجاع والاستبدال",
            "sections": [
                ("ضمان استبدال 30 يوم",
                 "كل قطعة تباع بضمان استبدال 30 يوماً. الضمان استبدال فقط ولا يوجد استرداد نقدي."),
                ("كيف تطلب الاستبدال",
                 "إذا ظهرت مشكلة في القطعة خلال 30 يوماً، اتصل بنا أو راسلنا على واتساب "
                 "058 232 8389. بعد التأكيد، تحضر القطعة إلى المعرض أو نأتي نحن لاستلامها "
                 "للإصلاح أو الاستبدال."),
                ("ما الذي يغطيه الضمان",
                 "الضمان يغطي الأعطال في القطعة أثناء استخدامك لها. لا يغطي الضمان الكسر أو "
                 "الضرر الناتج عن سوء الاستخدام."),
                ("جرّب قبل ما تشتري",
                 "يمكنك تجربة القطع في المعرض قبل الشراء — المكيفات (تبريد وتسخين) والثلاجات "
                 "(تبريد وتجميد). التجربة قبل الشراء تمنع أغلب حالات الاستبدال."),
            ],
        },
        "en": {
            "title": "Returns & Exchanges",
            "sections": [
                ("30-day exchange warranty",
                 "Every item comes with a 30-day exchange warranty. The warranty is exchange "
                 "only — there is no cash refund."),
                ("How to request an exchange",
                 "If a problem appears within 30 days, call us or write to us on WhatsApp "
                 "058 232 8389. After we confirm, bring the item to the showroom, or we pick "
                 "it up from you for repair or exchange."),
                ("What the warranty covers",
                 "The warranty covers faults in the item while it is in your use. It does not "
                 "cover breakage or damage caused by misuse."),
                ("Test before you buy",
                 "You can test items at the showroom before buying — ACs (cooling and heating) "
                 "and fridges (cooling and freezing). Testing before buying prevents most "
                 "returns."),
            ],
        },
    },
    "privacy": {
        "seo": {
            "ar_title": "سياسة الخصوصية | حراج تبوك للأثاث المستعمل",
            "en_title": "Privacy Policy | Tabuk Haraj Furniture",
            "ar_desc": (
                "نجمع فقط ما تكتبه في نماذجنا: الاسم والجوال والعنوان والرسالة — ولا نبيع "
                "بياناتك لأحد. تعرف على حقوقك في هذه الصفحة."
            ),
            "en_desc": (
                "We only collect what you type in our forms: name, phone, address and "
                "message — and we never sell your data. Learn about your rights here."
            ),
        },
        "ar": {
            "title": "سياسة الخصوصية",
            "sections": [
                ("ما الذي نجمعه",
                 "فقط ما تكتبه في نماذجنا: اسمك ورقم جوالك وعنوان التوصيل ورسالتك. كما نحفظ "
                 "ملف تعريف صغير (cookie) يتذكر لغتك المختارة (العربية أو الإنجليزية)."),
                ("كيف نستخدمه",
                 "نستخدم بياناتك للرد عليك فقط، وتأكيد طلبك، وتوصيله إليك."),
                ("لا نبيع بياناتك أبداً",
                 "لا نبيع بياناتك الشخصية ولا نؤجرها ولا نشاركها مع المعلنين أو شركات أخرى."),
                ("مدة الاحتفاظ",
                 "تبقى الرسائل في نظامنا لكي نخدمك. يمكنك طلب حذفها في أي وقت."),
                ("خياراتك",
                 "يمكنك معرفة بياناتنا لديك، أو طلب تصحيحها، أو طلب حذفها: "
                 "info@tabukharajfurniture.com أو اتصل على 058 232 8389."),
                ("تحديث هذه الصفحة",
                 "عند تغيير هذه السياسة نحدّث هذه الصفحة. آخر تحديث: أكتوبر 2026."),
            ],
        },
        "en": {
            "title": "Privacy Policy",
            "sections": [
                ("What we collect",
                 "Only what you type into our forms: your name, phone number, delivery address "
                 "and message. We also store one small cookie that remembers your language "
                 "choice (Arabic or English)."),
                ("How we use it",
                 "We use your details only to answer you, confirm your order and deliver to you."),
                ("We never sell your data",
                 "We do not sell, rent or share your personal data with advertisers or other "
                 "companies."),
                ("How long we keep it",
                 "Messages stay in our system while we need them to serve you. You can ask us "
                 "to delete them at any time."),
                ("Your choices",
                 "You can ask what data we hold, ask for a correction, or ask us to delete it: "
                 "info@tabukharajfurniture.com or call 058 232 8389."),
                ("Changes to this page",
                 "If this policy changes, we update this page. Last updated: October 2026."),
            ],
        },
    },
    "terms": {
        "seo": {
            "ar_title": "الشروط والأحكام | حراج تبوك للأثاث المستعمل",
            "en_title": "Terms of Service | Tabuk Haraj Furniture",
            "ar_desc": (
                "شروط الشراء من حراج تبوك للأثاث: المنتجات والأسعار، طلبات الشراء، طرق الدفع، "
                "الضمان 30 يوم، والتوصيل داخل تبوك."
            ),
            "en_desc": (
                "Shopping terms for Tabuk Haraj Furniture: products and prices, order requests, "
                "payment methods, 30-day warranty and delivery inside Tabuk."
            ),
        },
        "ar": {
            "title": "الشروط والأحكام",
            "sections": [
                ("من نحن",
                 "حراج تبوك للأثاث معرض لأثاث وأجهزة مستعملة في تبوك، السعودية. رقم الرخصة "
                 "التجارية 470220635950. المعرض: المنشية القديمة، طريق معاوية، تبوك 47914."),
                ("المنتجات والأسعار",
                 "جميع القطع مستعملة وتُفحص قبل البيع. الأسعار بالريال السعودي وقد تتغير دون "
                 "إشعار. القطع متوفرة حسب المخزون — صفحة المنتج تعرض حالة القطع الحالية "
                 "(متوفر، محجوز، أو مباع)."),
                ("طلبات الشراء",
                 "إرسال طلب مباشر أو رسالة أو واتساب يعتبر طلباً وليس عملية شراء مؤكدة. نتصل "
                 "بك أو نراسلك لتأكيد القطعة والسعر النهائي والتوصيل."),
                ("طرق الدفع",
                 "نقبل النقد، مدى وفيزا، التحويل البنكي، STC Pay، Apple Pay، والتقسيط عبر تمارا."),
                ("الضمان والتوصيل",
                 "كل قطعة بضمان استبدال 30 يوماً والتوصيل مجاني داخل تبوك. راجع صفحتي التوصيل "
                 "والاسترجاع للتفاصيل."),
                ("تواصل معنا",
                 "الهاتف والواتساب: 058 232 8389. البريد الإلكتروني: "
                 "info@tabukharajfurniture.com. المعرض: المنشية القديمة، طريق معاوية، تبوك 47914."),
            ],
        },
        "en": {
            "title": "Terms of Service",
            "sections": [
                ("Who we are",
                 "Tabuk Haraj Furniture is a used furniture and appliances showroom in Tabuk, "
                 "Saudi Arabia. Commercial license 470220635950. Showroom: Al Munshiyah Al "
                 "Qadimah, Muawiyah Road, Tabuk 47914."),
                ("Products and prices",
                 "All items are used and checked before sale. Prices are in Saudi Riyals (SAR) "
                 "and may change without notice. Items are subject to availability — the product "
                 "page always shows the current status (available, reserved or sold)."),
                ("Order requests",
                 "Sending a Direct Order, a message or a WhatsApp is a request, not a confirmed "
                 "purchase. We call or message you to confirm the item, the final price and the "
                 "delivery."),
                ("Payment methods",
                 "We accept cash, mada and Visa cards, bank transfer, STC Pay, Apple Pay, and "
                 "installments with Tamara."),
                ("Warranty and delivery",
                 "Every item comes with a 30-day exchange warranty and delivery is free inside "
                 "Tabuk. See our Delivery and Returns pages for details."),
                ("Contact us",
                 "Phone and WhatsApp: 058 232 8389. Email: info@tabukharajfurniture.com. "
                 "Showroom: Al Munshiyah Al Qadimah, Muawiyah Road, Tabuk 47914."),
            ],
        },
    },
}

_POLICY_SCHEMA_TYPE = {"privacy": "PrivacyPolicy", "terms": "TermsOfService"}


def policy(request, page):
    """Render one of the four static policy pages (shipping, returns,
    privacy, terms) with its own title, body and WebPage schema."""
    data = _POLICIES[page]
    _set_seo(request, **data["seo"])
    body = data["en"] if _is_en() else data["ar"]
    page_url = CANONICAL + reverse(f"pages:{page}")
    return render(request, "pages/policy.html", {
        "policy_title": body["title"],
        "policy_sections": [{"h": h, "p": p} for h, p in body["sections"]],
        "policy_url": page_url,
        "policy_schema_type": _POLICY_SCHEMA_TYPE.get(page, "WebPage"),
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

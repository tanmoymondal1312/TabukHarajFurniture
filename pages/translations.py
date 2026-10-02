"""UI text translations for the public site.

English text in the templates is the source (msgid). This map holds the
Arabic version of each string. Language "en" always falls back to the
source text, so the English site needs no entries here.

Only static UI strings live here. Product titles, category names and
other database content are never translated.

Placeholders use printf style: %(name)s
"""

TRANSLATIONS = {
    "ar": {
        # ---- Header / navigation ----
        "Home": "الرئيسية",
        "Products": "المنتجات",
        "About": "من نحن",
        "FAQ": "الأسئلة الشائعة",
        "Contact": "تواصل معنا",
        "Visit Showroom": "زيارة المعرض",
        "Main": "القائمة الرئيسية",
        "Open menu": "فتح القائمة",
        "Close menu": "إغلاق القائمة",

        # ---- Footer ----
        "Follow Us": "تابعونا",
        "WhatsApp Chat": "محادثة واتساب",
        "© 2026 Tabuk Haraj Furniture. All rights reserved.": "© 2026 حراج تبوك للأثاث. جميع الحقوق محفوظة.",

        # ---- Hero ----
        "30-Day Warranty • Free Delivery": "ضمان 30 يوم • توصيل مجاني",
        "Tabuk Haraj for Used Furniture<br>Physical Showroom in <span class=\"hero__title-gold\">Tabuk</span>":
            "حراج تبوك للأثاث المستعمل<br>معرض فعلي في <span class=\"hero__title-gold\">تبوك</span>",
        "Buy tested used furniture & ACs — 30-day warranty & free delivery":
            "أثاث ومكيفات مستعملة مفحوصة — ضمان 30 يوم وتوصيل مجاني",
        "Also selling? We buy yours — instant cash, free pickup":
            "تبيع أيضاً؟ نشتري منك — نقداً فوراً واستلام مجاني",
        "Search for furniture, appliances, or categories...": "ابحث عن أثاث أو أجهزة أو أقسام...",
        "Search listings": "البحث عن الأثاث",
        "Tabuk": "تبوك",
        "Search": "بحث",
        "Popular searches:": "الأكثر بحثاً:",
        "Used Sofa": "أريكة مستعملة",
        "AC": "مكيف",
        "Fridge": "ثلاجة",
        "Majlis": "مجلس",
        "Bedroom Set": "غرفة نوم",
        "Carousel pagination": "تنقل الشرائح",
        "Previous slide": "الشريحة السابقة",
        "Next slide": "الشريحة التالية",
        "Go to slide": "الشريحة",

        # ---- Trust strip ----
        "Trusted Sellers": "بائعون موثوقون",
        "Buy with confidence": "اشترِ بثقة",
        "Fast Delivery": "توصيل سريع",
        "Across Tabuk": "في جميع أنحاء تبوك",
        "Best Prices": "أفضل الأسعار",
        "Great deals everyday": "عروض ممتازة كل يوم",
        "Visit Our Showroom": "زوروا معرضنا",
        "See it in person": "شاهدها بنفسك",

        # ---- Categories section (home) ----
        "Explore Categories": "استكشف الأقسام",
        "Shop by Category": "تسوق حسب القسم",
        "View All Categories": "عرض جميع الأقسام",
        "%(n)s items": "%(n)s عنصر",

        # ---- Listings section (home) ----
        "Featured Listings": "إعلانات مميزة",
        "Hot Deals Right Now": "عروض ساخنة الآن",
        "View All Products": "عرض جميع المنتجات",

        # ---- Products page ----
        "Our Products": "منتجاتنا",
        "All Products": "كل المنتجات",
        "Quality used furniture and appliances in Tabuk. Every item is tested, comes with a 30-day warranty and free delivery.":
            "أثاث وأجهزة مستعملة بجودة عالية في تبوك. كل قطعة مفحوصة، مع ضمان 30 يوم وتوصيل مجاني.",
        "%(n)s product%(plural)s in stock": "%(n)s منتج متوفر",
        "Categories": "الأقسام",
        "Categories:": "الأقسام:",
        "Category filter": "تصفية الأقسام",
        "All": "الكل",
        "Showing": "عرض",
        "of %(total)s product%(plural)s": "من %(total)s منتج",
        "Search…": "ابحث…",
        "Search products": "البحث في المنتجات",
        "Featured": "مميز",
        "No products found": "لم يتم العثور على منتجات",
        "No products in this category yet": "لا توجد منتجات في هذا القسم بعد",
        "Nothing matches “%(q)s”. Try another word, or browse all products.":
            "لا توجد نتائج لـ “%(q)s”. جرّب كلمة أخرى، أو تصفح كل المنتجات.",
        "This category is empty right now. Browse all products instead.":
            "هذا القسم فارغ حالياً. تصفح جميع المنتجات بدلاً من ذلك.",
        "Close categories": "إغلاق الأقسام",
    },
}

# Languages the site can show. "en" is the source language of the templates.
AVAILABLE_LANGUAGES = ("ar", "en")

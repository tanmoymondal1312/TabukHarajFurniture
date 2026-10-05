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
        "Call Now": "اتصل الآن",
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

        # ---- Condition / status / product details ----
        "Used": "مستعمل",
        "Like New": "شبه جديد",
        "New": "جديد",
        "Available": "متوفر",
        "Reserved": "محجوز",
        "Sold": "مباع",
        "Category": "القسم",
        "Condition": "الحالة",
        "Status": "التوفّر",
        "Price": "السعر",
        "Location": "الموقع",
        "Listed": "تاريخ العرض",
        "Product Description": "وصف المنتج",
        "Item Details": "تفاصيل المنتج",
        "You may also like": "قد يعجبك أيضاً",
        "Related Products": "منتجات مشابهة",
        "Chat on WhatsApp": "دردشة واتساب",
        "30-day warranty": "ضمان 30 يوم",
        "30-day warranty on every item": "ضمان 30 يوم على كل قطعة",
        "Free delivery across Tabuk": "توصيل مجاني في جميع أنحاء تبوك",
        "Test the item before you buy": "جرّب القطعة قبل الشراء",
        "%(n)s%% OFF": "خصم %(n)s٪",

        # ---- Direct order (product page) ----
        "Direct Order": "طلب مباشر",
        "Fill your details and we will call you to confirm the order.":
            "اكتب بياناتك وسنتصل بك لتأكيد الطلب.",
        "Full Name": "الاسم الكامل",
        "Phone Number": "رقم الجوال",
        "Delivery Address": "عنوان التوصيل",
        "Notes (optional)": "ملاحظات (اختياري)",
        "Send Order Request": "إرسال الطلب",
        "Your order request has been sent. We will call you soon.":
            "تم إرسال طلبك. سنتصل بك قريباً.",
        "Please write your name.": "اكتب اسمك من فضلك.",
        "Please write your phone number.": "اكتب رقم الجوال من فضلك.",
        "Phone number is not valid. Example: 0582328389":
            "رقم الجوال غير صحيح. مثال: 0582328389",
        "Please write your delivery address.": "اكتب عنوان التوصيل من فضلك.",
        "Something went wrong. Please try again.": "حدث خطأ، حاول مرة أخرى.",
        "Close": "إغلاق",

        # ---- FAQ blocks (products + product page) ----
        "Frequently Asked Questions": "الأسئلة الشائعة",
        "Quick answers": "إجابات سريعة",
        "Common questions": "أسئلة متكررة",
        "Do your items come with a warranty?": "هل القطع المتوفرة لديكم تحتوي على ضمان؟",
        "Yes — every item comes with a 30-day exchange warranty. There is no cash refund. If a problem appears within 30 days, bring the item to the showroom or we pick it up for repair or exchange.":
            "نعم — كل قطعة تأتي بضمان استبدال 30 يوماً ولا يوجد استرداد نقدي. إذا ظهرت مشكلة خلال 30 يوماً، تحضر القطعة إلى المعرض أو نستلمها نحن للإصلاح أو الاستبدال.",
        "Is delivery free?": "هل التوصيل مجاني؟",
        "Yes — delivery is free across all Tabuk districts, usually the same day or the next day.":
            "نعم — التوصيل مجاني لجميع أحياء تبوك، عادةً في نفس اليوم أو اليوم التالي.",
        "Can I test an item before buying?": "هل يمكن تجربة القطعة قبل الشراء؟",
        "Yes — you can test items at the showroom before buying. ACs are tested for cooling and heating, and fridges for cooling and freezing.":
            "نعم — يمكنكم تجربة القطع داخل المعرض قبل الشراء. تُجرب المكيفات (تبريد وتسخين) والثلاجات (تبريد وتجميد).",
        "What payment methods do you accept?": "ما هي طرق الدفع المقبولة؟",
        "We accept cash, mada and Visa cards, bank transfer, STC Pay, Apple Pay, and installments with Tamara.":
            "نقبل النقد، مدى وفيزا، التحويل البنكي، STC Pay، Apple Pay، والتقسيط عبر تمارا.",
        "Are the items new or used?": "هل القطع جديدة أم مستعملة؟",
        "All items are used but checked and cleaned. Every piece is tested before listing, ready to use with a 30-day warranty.":
            "جميع القطع مستعملة لكنها مفحوصة ونظيفة. كل قطعة تُختبر قبل عرضها، وجاهزة للاستخدام مع ضمان 30 يوم.",
        "Before you buy": "قبل الشراء",
        "Questions about this item": "أسئلة عن هذه القطعة",
        "Is %(t)s under warranty?": "هل يشمل %(t)s ضماناً؟",
        "Can I test this item before buying?": "هل يمكنني تجربة هذه القطعة قبل الشراء؟",
        "Is delivery free for this item?": "هل التوصيل مجاني لهذه القطعة؟",
        "How can I order this item?": "كيف أطلب هذه القطعة؟",
        "Press the Direct Order button on this page, or contact us on WhatsApp at 0582328389 or by phone. We will confirm the item and delivery with you.":
            "اضغط زر الطلب المباشر في هذه الصفحة، أو تواصل معنا على واتساب 0582328389 أو بالهاتف. سنؤكد لك القطعة والتوصيل.",

        # ---- Policy pages + footer info column ----
        "Information": "معلومات",
        "Customer Care": "خدمة العملاء",
        "Related pages": "صفحات ذات صلة",
        "Delivery & Pickup": "التوصيل والاستلام",
        "Returns & Exchanges": "الاسترجاع والاستبدال",
        "Privacy Policy": "سياسة الخصوصية",
        "Terms of Service": "الشروط والأحكام",

        # ---- /sell/ page (we buy used furniture) ----
        "Sell to us": "نشتري منك",
        "Simple steps": "خطوات بسيطة",
        "Reply within an hour": "رد خلال ساعة",
        "Your name": "اسمك",
        "What do you want to sell?": "ماذا تريد أن تبيع؟",
        "Example: 3-seat sofa in good condition, Al Nakheel district":
            "مثال: كنب 3 مقاعد بحالة جيدة، حي النخيل",
        "Send Price Request": "إرسال طلب السعر",
        "Your request has been sent": "تم إرسال طلبك",
        "We will contact you soon with a price offer.": "سنتواصل معك قريباً مع عرض السعر.",
        "Check the required fields": "راجع الحقول المطلوبة",
        "Your details reach us only — we never share them.":
            "بياناتك تصل إلينا فقط — لا نشاركها مع أي جهة.",

        # ---- District landing pages ----
        "Districts we serve": "الأحياء التي نخدمها",
        "Free delivery • 30-day warranty • Cash on delivery":
            "توصيل مجاني • ضمان 30 يوم • الدفع عند الاستلام",
        "Available now": "متاح الآن",
    },
}

# Languages the site can show. "en" is the source language of the templates.
AVAILABLE_LANGUAGES = ("ar", "en")

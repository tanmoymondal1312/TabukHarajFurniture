"""
Context processors for SEO and business information
"""
from urllib.parse import urlencode

from django.conf import settings
from django.utils.translation import get_language

# Query params that should never appear in a canonical URL:
# search results (q), form feedback (sent) and tracking tags (utm_*).
_DROP_PARAMS = {"q", "sent"}


def business_info(request):
    """Make business information available in all templates"""
    return {
        'business_info': getattr(settings, 'BUSINESS_INFO', {}),
        'site_name': getattr(settings, 'SITE_NAME', 'Tabuk Haraj Furniture'),
        'site_domain': getattr(settings, 'SITE_DOMAIN', 'tabukharajfurniture.com'),
        'site_url': getattr(settings, 'SITE_URL', 'https://tabukharajfurniture.com'),
    }


def _is_en():
    return (get_language() or "ar").split("-")[0].lower() == "en"


def seo_context(request):
    """Add SEO-related context variables.

    canonical_url is the preferred URL of the current page:
    search/tracking params are removed, the language stays (each
    language version is canonical for itself so hreflang pairs work).
    hreflang_ar / hreflang_en are the two language versions of the
    current page, used for the rel=alternate links in <head>.
    """
    site = getattr(settings, 'SITE_URL', 'https://tabukharajfurniture.com')

    kept = [
        (key, value)
        for key, values in request.GET.lists()
        for value in values
        if key not in _DROP_PARAMS and not key.startswith("utm_")
    ]
    ar_items = [(k, v) for k, v in kept if k != "lang"]
    en_items = ar_items + [("lang", "en")]

    def build(items):
        query = urlencode(items)
        return site + request.path + ("?" + query if query else "")

    return {
        'current_url': request.build_absolute_uri(),
        'canonical_url': build(kept),
        'hreflang_ar': build(ar_items),
        'hreflang_en': build(en_items),
        'page_title': getattr(request, 'page_title', ''),
        'page_description': getattr(request, 'page_description', ''),
        'page_image': getattr(request, 'page_image', ''),
    }

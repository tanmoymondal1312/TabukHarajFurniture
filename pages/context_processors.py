"""
Context processors for SEO and business information
"""
from django.conf import settings


def business_info(request):
    """Make business information available in all templates"""
    return {
        'business_info': getattr(settings, 'BUSINESS_INFO', {}),
        'site_name': getattr(settings, 'SITE_NAME', 'Tabuk Haraj Furniture'),
        'site_domain': getattr(settings, 'SITE_DOMAIN', 'tabukharajfurniture.com'),
        'site_url': getattr(settings, 'SITE_URL', 'https://tabukharajfurniture.com'),
    }


def seo_context(request):
    """Add SEO-related context variables"""
    return {
        'current_url': request.build_absolute_uri(),
        'canonical_url': request.build_absolute_uri(),
        'page_title': getattr(request, 'page_title', ''),
        'page_description': getattr(request, 'page_description', ''),
        'page_image': getattr(request, 'page_image', ''),
    }
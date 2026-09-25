"""
Sitemap configuration for Tabuk Haraj Furniture
"""
from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class StaticViewSitemap(Sitemap):
    """Sitemap for static pages"""
    priority = 1.0
    changefreq = 'daily'

    def items(self):
        return ['pages:home']

    def location(self, item):
        return reverse(item)


class CategorySitemap(Sitemap):
    """Sitemap for category pages"""
    priority = 0.8
    changefreq = 'weekly'

    def items(self):
        return [
            'majlis-sofas',
            'bedroom-sets',
            'dining-tables',
            'home-appliances',
            'kitchen-furniture',
            'other-furniture',
        ]

    def location(self, item):
        return f'/?q={item}'

    def lastmod(self, item):
        from django.utils import timezone
        return timezone.now()


class ListingSitemap(Sitemap):
    """Sitemap for individual listings"""
    priority = 0.6
    changefreq = 'daily'

    def items(self):
        # This would be replaced with actual database listings
        return []

    def location(self, item):
        return item.get_absolute_url()

    def lastmod(self, item):
        return item.updated_at if hasattr(item, 'updated_at') else None


# Sitemaps dictionary
sitemaps = {
    'static': StaticViewSitemap,
    'categories': CategorySitemap,
    'listings': ListingSitemap,
}
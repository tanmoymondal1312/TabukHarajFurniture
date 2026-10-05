"""
Sitemap configuration for Tabuk Haraj Furniture.

Only pages a visitor can actually open are listed:
active categories and products whose category is active.
"""
from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from .models import Category, Product
from .views import _DISTRICT_SLUGS

# (view name, priority, changefreq) for the static pages.
_STATIC_PAGES = [
    ("pages:home", "1.0", "daily"),
    ("pages:products", "0.9", "daily"),
    ("pages:about", "0.6", "monthly"),
    ("pages:faq", "0.6", "monthly"),
    ("pages:contact", "0.6", "monthly"),
    ("pages:sell", "0.8", "weekly"),
    ("pages:shipping", "0.6", "yearly"),
    ("pages:returns", "0.6", "yearly"),
    ("pages:privacy", "0.4", "yearly"),
    ("pages:terms", "0.4", "yearly"),
] + [
    (f"pages:district_{slug}", "0.7", "weekly") for slug in _DISTRICT_SLUGS
]


class StaticViewSitemap(Sitemap):
    """Sitemap for the static pages (home, products, about, faq, contact)."""
    protocol = "https"

    def items(self):
        return [name for name, _, _ in _STATIC_PAGES]

    def location(self, item):
        return reverse(item)

    def priority(self, item):
        return dict((name, p) for name, p, _ in _STATIC_PAGES)[item]

    def changefreq(self, item):
        return dict((name, c) for name, _, c in _STATIC_PAGES)[item]


class CategorySitemap(Sitemap):
    """Sitemap for active category pages (/products/?cat=slug)."""

    protocol = "https"
    priority = 0.7
    changefreq = "weekly"

    def items(self):
        return Category.objects.filter(is_active=True)

    def location(self, item):
        return f"{reverse('pages:products')}?cat={item.slug}"

    def lastmod(self, item):
        return item.updated_at


class ProductSitemap(Sitemap):
    """Sitemap for product pages that are visible on the site."""

    protocol = "https"
    priority = 0.6
    changefreq = "weekly"

    def items(self):
        return Product.objects.filter(
            is_active=True,
            status=Product.STATUS_AVAILABLE,
            category__is_active=True,
        )

    def location(self, item):
        return item.get_absolute_url()

    def lastmod(self, item):
        return item.updated_at


# Sitemaps dictionary
sitemaps = {
    "static": StaticViewSitemap,
    "categories": CategorySitemap,
    "products": ProductSitemap,
}

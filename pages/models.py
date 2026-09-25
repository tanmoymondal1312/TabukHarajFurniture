from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    """A product category shown on the homepage grid."""

    name = models.CharField(max_length=100, unique=True)
    ar_name = models.CharField(max_length=100, blank=True, help_text="Arabic name (optional)")
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    image = models.ImageField(upload_to="categories/", blank=True, null=True)
    description = models.TextField(blank=True)
    ordering = models.PositiveIntegerField(default=0, help_text="Lower numbers show first")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["ordering", "name"]
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    @property
    def item_count(self):
        # Listings are not in the database yet.
        # When the Listing model exists, count them here instead.
        return 0

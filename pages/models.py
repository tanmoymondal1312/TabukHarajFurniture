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
        return self.products.filter(is_active=True, status=Product.STATUS_AVAILABLE).count()


class Product(models.Model):
    """A used product (furniture, appliance...) sold by the shop."""

    CONDITION_USED = "used"
    CONDITION_LIKE_NEW = "like_new"
    CONDITION_NEW = "new"
    CONDITION_CHOICES = [
        (CONDITION_USED, "Used"),
        (CONDITION_LIKE_NEW, "Like New"),
        (CONDITION_NEW, "New"),
    ]

    STATUS_AVAILABLE = "available"
    STATUS_RESERVED = "reserved"
    STATUS_SOLD = "sold"
    STATUS_CHOICES = [
        (STATUS_AVAILABLE, "Available"),
        (STATUS_RESERVED, "Reserved"),
        (STATUS_SOLD, "Sold"),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, related_name="products"
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    old_price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True,
        help_text="Leave empty for no discount",
    )
    condition = models.CharField(
        max_length=20, choices=CONDITION_CHOICES, default=CONDITION_USED
    )
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="products/", blank=True, null=True)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default=STATUS_AVAILABLE
    )
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(
        default=False, help_text="Shows in Hot Deals Right Now"
    )
    location = models.CharField(max_length=100, default="Tabuk")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    @property
    def has_discount(self):
        return self.old_price is not None and self.old_price > self.price

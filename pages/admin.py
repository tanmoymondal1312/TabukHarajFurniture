from django.contrib import admin

from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "ar_name", "ordering", "is_active", "updated_at")
    list_editable = ("ordering", "is_active")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name", "ar_name")
    list_filter = ("is_active",)
    ordering = ("ordering", "name")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "price", "condition", "status",
                    "is_featured", "is_active", "created_at")
    list_editable = ("status", "is_featured", "is_active")
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ("title", "description")
    list_filter = ("status", "condition", "is_active", "is_featured", "category")
    list_select_related = ("category",)
    ordering = ("-created_at",)

from django.contrib import admin

from .models import Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "ar_name", "ordering", "is_active", "updated_at")
    list_editable = ("ordering", "is_active")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name", "ar_name")
    list_filter = ("is_active",)
    ordering = ("ordering", "name")

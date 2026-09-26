from django import forms

from pages.models import Category, Product

INPUT = {"class": "input"}
SELECT = {"class": "input input--select"}
TEXTAREA = {"class": "input input--area"}


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            "title", "category", "price", "old_price", "condition",
            "description", "image", "status", "is_featured", "is_active",
            "location",
        ]
        widgets = {
            "title": forms.TextInput(attrs={
                **INPUT, "placeholder": "e.g. Used Wooden Dining Table for 6",
            }),
            "category": forms.Select(attrs=SELECT),
            "price": forms.NumberInput(attrs={
                **INPUT, "placeholder": "1800", "step": "0.01", "min": "0",
            }),
            "old_price": forms.NumberInput(attrs={
                **INPUT, "placeholder": "Optional — must be higher than price",
                "step": "0.01", "min": "0",
            }),
            "condition": forms.Select(attrs=SELECT),
            "description": forms.Textarea(attrs={
                **TEXTAREA, "rows": 6,
                "placeholder": "Describe the item: size, material, age, any flaws...",
            }),
            "image": forms.ClearableFileInput(attrs={
                "class": "input input--file", "accept": "image/*",
            }),
            "status": forms.Select(attrs=SELECT),
            "is_featured": forms.CheckboxInput(attrs={"class": "switch-input"}),
            "is_active": forms.CheckboxInput(attrs={"class": "switch-input"}),
            "location": forms.TextInput(attrs={**INPUT, "placeholder": "Tabuk"}),
        }

    def clean(self):
        cleaned = super().clean()
        price = cleaned.get("price")
        old_price = cleaned.get("old_price")
        if price is not None and old_price is not None and old_price <= price:
            raise forms.ValidationError(
                "Old price must be higher than the selling price "
                "(it shows the discount)."
            )
        return cleaned


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name", "ar_name", "slug", "image", "description", "ordering", "is_active"]
        widgets = {
            "name": forms.TextInput(attrs={**INPUT, "placeholder": "e.g. Air Conditioners"}),
            "ar_name": forms.TextInput(attrs={
                **INPUT, "dir": "rtl", "placeholder": "مكيفات (optional)",
            }),
            "slug": forms.TextInput(attrs={
                **INPUT, "placeholder": "Leave empty to fill from name",
            }),
            "image": forms.ClearableFileInput(attrs={
                "class": "input input--file", "accept": "image/*",
            }),
            "description": forms.Textarea(attrs={
                **TEXTAREA, "rows": 4, "placeholder": "Short text for this category (optional)",
            }),
            "ordering": forms.NumberInput(attrs={**INPUT, "min": "0", "placeholder": "0"}),
            "is_active": forms.CheckboxInput(attrs={"class": "switch-input"}),
        }

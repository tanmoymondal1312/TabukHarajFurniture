from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator
from django.db.models import Count, Q, Sum
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_POST

from pages.models import Category, Product

from .forms import CategoryForm, ProductForm

NO_PHOTO_Q = Q(image__isnull=True) | Q(image="")


class DashboardLoginView(LoginView):
    template_name = "dashboard/login.html"
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse("dashboard:overview")


@require_POST
def logout_view(request):
    logout(request)
    return redirect("dashboard:login")


@login_required
def overview(request):
    products = Product.objects.all()
    stats = {
        "total": products.count(),
        "available": products.filter(status=Product.STATUS_AVAILABLE).count(),
        "reserved": products.filter(status=Product.STATUS_RESERVED).count(),
        "sold": products.filter(status=Product.STATUS_SOLD).count(),
        "featured": products.filter(is_featured=True).count(),
        "categories": Category.objects.filter(is_active=True).count(),
        "value": products.filter(status=Product.STATUS_AVAILABLE)
                    .aggregate(v=Sum("price"))["v"] or 0,
        "no_photo": products.filter(NO_PHOTO_Q).count(),
    }
    context = {
        "active": "overview",
        "stats": stats,
        "recent": products.select_related("category")[:8],
        "cat_stats": Category.objects.annotate(n=Count("products")).order_by("ordering"),
        "max_cat": max([c.n for c in Category.objects.annotate(n=Count("products"))] or [1]),
    }
    return render(request, "dashboard/overview.html", context)


@login_required
def product_list(request):
    qs = Product.objects.select_related("category")
    q = request.GET.get("q", "").strip()
    status = request.GET.get("status", "")
    cat_id = request.GET.get("category", "")

    if q:
        qs = qs.filter(Q(title__icontains=q) | Q(description__icontains=q))
    if status in dict(Product.STATUS_CHOICES):
        qs = qs.filter(status=status)
    if cat_id.isdigit():
        qs = qs.filter(category_id=cat_id)

    page = Paginator(qs, 12).get_page(request.GET.get("page"))
    context = {
        "active": "products",
        "page": page,
        "q": q,
        "status": status,
        "cat_id": cat_id,
        "categories": Category.objects.all(),
        "status_choices": Product.STATUS_CHOICES,
        "condition_choices": Product.CONDITION_CHOICES,
    }
    return render(request, "dashboard/product_list.html", context)


def _product_form(request, instance=None):
    title = "Edit Product" if instance else "Add Product"
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            product = form.save()
            messages.success(request, f"“{product.title}” saved.")
            return redirect("dashboard:product_list")
    else:
        form = ProductForm(instance=instance)
    return render(request, "dashboard/product_form.html", {
        "active": "products",
        "form": form,
        "title": title,
        "product": instance,
        "categories": Category.objects.all(),
    })


@login_required
def product_create(request):
    return _product_form(request)


@login_required
def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return _product_form(request, instance=product)


@login_required
@require_POST
def product_action(request, pk):
    product = get_object_or_404(Product, pk=pk)
    action = request.POST.get("action", "")
    if action == "mark_sold":
        product.status = Product.STATUS_SOLD
        note = "marked as sold"
    elif action == "mark_available":
        product.status = Product.STATUS_AVAILABLE
        note = "marked as available"
    elif action == "mark_reserved":
        product.status = Product.STATUS_RESERVED
        note = "marked as reserved"
    elif action == "toggle_featured":
        product.is_featured = not product.is_featured
        note = "hot deal on" if product.is_featured else "hot deal off"
    elif action == "toggle_active":
        product.is_active = not product.is_active
        note = "visible on site" if product.is_active else "hidden from site"
    else:
        messages.error(request, "Unknown action.")
        return redirect("dashboard:product_list")
    product.save()
    messages.success(request, f"“{product.title}” {note}.")
    return redirect("dashboard:product_list")


@login_required
@require_POST
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    title = product.title
    product.delete()
    messages.success(request, f"“{title}” deleted.")
    return redirect("dashboard:product_list")


@login_required
def category_list(request):
    categories = Category.objects.annotate(n=Count("products"))
    context = {
        "active": "categories",
        "categories": categories,
        "total_products": Product.objects.count(),
    }
    return render(request, "dashboard/category_list.html", context)


def _category_form(request, instance=None):
    title = "Edit Category" if instance else "Add Category"
    if request.method == "POST":
        form = CategoryForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            category = form.save()
            messages.success(request, f"Category “{category.name}” saved.")
            return redirect("dashboard:category_list")
    else:
        form = CategoryForm(instance=instance)
    return render(request, "dashboard/category_form.html", {
        "active": "categories",
        "form": form,
        "title": title,
        "category": instance,
    })


@login_required
def category_create(request):
    return _category_form(request)


@login_required
def category_edit(request, pk):
    category = get_object_or_404(Category, pk=pk)
    return _category_form(request, instance=category)


@login_required
@require_POST
def category_action(request, pk):
    category = get_object_or_404(Category, pk=pk)
    action = request.POST.get("action", "")
    if action == "toggle_active":
        category.is_active = not category.is_active
        category.save(update_fields=["is_active"])
        messages.success(
            request,
            f"“{category.name}” " + ("activated." if category.is_active else "deactivated."),
        )
    elif action in ("up", "down"):
        current = list(Category.objects.all())
        index = next((i for i, c in enumerate(current) if c.pk == category.pk), None)
        other = index - 1 if action == "up" else index + 1
        if index is not None and 0 <= other < len(current):
            a, b = current[index], current[other]
            a.ordering, b.ordering = b.ordering, a.ordering
            if a.ordering == b.ordering:
                a.ordering, b.ordering = other + 1, index + 1
            a.save(update_fields=["ordering"])
            b.save(update_fields=["ordering"])
            messages.success(request, f"“{category.name}” moved {action}.")
    return redirect("dashboard:category_list")


@login_required
@require_POST
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if Product.objects.filter(category=category).exists():
        messages.error(
            request,
            f"“{category.name}” still has products. "
            "Move or delete them first.",
        )
        return redirect("dashboard:category_list")
    name = category.name
    category.delete()
    messages.success(request, f"Category “{name}” deleted.")
    return redirect("dashboard:category_list")

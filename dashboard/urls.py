from django.urls import path

from . import views

app_name = "dashboard"

urlpatterns = [
    path("login/", views.DashboardLoginView.as_view(), name="login"),
    path("logout/", views.logout_view, name="logout"),

    path("", views.overview, name="overview"),

    path("products/", views.product_list, name="product_list"),
    path("products/add/", views.product_create, name="product_create"),
    path("products/<int:pk>/edit/", views.product_edit, name="product_edit"),
    path("products/<int:pk>/action/", views.product_action, name="product_action"),
    path("products/<int:pk>/delete/", views.product_delete, name="product_delete"),

    path("categories/", views.category_list, name="category_list"),
    path("categories/add/", views.category_create, name="category_create"),
    path("categories/<int:pk>/edit/", views.category_edit, name="category_edit"),
    path("categories/<int:pk>/action/", views.category_action, name="category_action"),
    path("categories/<int:pk>/delete/", views.category_delete, name="category_delete"),
]

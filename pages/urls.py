from django.urls import path

from . import views

app_name = "pages"

urlpatterns = [
    path("", views.home, name="home"),
    path("faq/", views.faq, name="faq"),
    path("products/", views.products, name="products"),
    path("product/<slug:slug>/", views.product_detail, name="product"),
]

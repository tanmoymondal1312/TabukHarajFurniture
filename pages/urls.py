from django.urls import path

from . import views

app_name = "pages"

urlpatterns = [
    path("", views.home, name="home"),
    path("faq/", views.faq, name="faq"),
    path("products/", views.products, name="products"),
    path("product/<slug:slug>/", views.product_detail, name="product"),
    path("product/<slug:slug>/order/", views.product_order, name="product_order"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path("sell/", views.sell, name="sell"),
    path("reviews/", views.reviews, name="reviews"),
    path("shipping/", views.policy, {"page": "shipping"}, name="shipping"),
    path("returns/", views.policy, {"page": "returns"}, name="returns"),
    path("privacy/", views.policy, {"page": "privacy"}, name="privacy"),
    path("terms/", views.policy, {"page": "terms"}, name="terms"),
]

# One landing page per Tabuk district: /nakheel/, /hasah/, ...
for _slug in views._DISTRICT_SLUGS:
    urlpatterns.append(
        path(f"{_slug}/", views.district, {"slug": _slug}, name=f"district_{_slug}")
    )

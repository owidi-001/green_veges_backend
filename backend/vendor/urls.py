from django.contrib.auth.views import LoginView
from django.urls import path

from .views import dashboard_register, dashboard_login, dashboard_analytics, dashboard_products, dashboard_contact, \
    edit_product

urlpatterns = [
    path("", dashboard_login, name="login"),
    path("register", dashboard_register, name="register"),
    path("analytics", dashboard_analytics, name="analytics"),
    path("products", dashboard_products, name="products"),
    path("products/<int:id>/edit", edit_product, name="product_edit"),
    path("contact", dashboard_contact, name="contact"),
    # path("vendor/", VendorViews.as_view(), name="vendor"),
]

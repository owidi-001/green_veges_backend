from django.conf import settings
from django.contrib.auth.views import LogoutView
from django.urls import path

from .views import (dashboard_register, dashboard_login, dashboard_analytics, dashboard_products, dashboard_contact, \
    edit_product, create_product, dashboard_orders, manage_orders, delete_product, VendorViews)

urlpatterns = [
    path("logout/", LogoutView.as_view(), {'next_page': settings.LOGOUT_REDIRECT_URL}, name='logout'),
    path("", dashboard_login, name="login"),
    path("register", dashboard_register, name="register"),
    path("analytics", dashboard_analytics, name="analytics"),
    path("products", dashboard_products, name="products"),
    path("products/new", create_product, name="create_product"),
    path("products/<int:id>/edit", edit_product, name="product_edit"),
    path("products/<int:id>/delete", delete_product, name="product_delete"),
    path("vendor/orders", dashboard_orders, name="vendor_orders"),
    path("orders/<int:id>/manage", manage_orders, name="manage_orders"),
    path("contact", dashboard_contact, name="contact"),

    # Vendor api for app
    path("vendors/", VendorViews.as_view(), name="vendor"),
]

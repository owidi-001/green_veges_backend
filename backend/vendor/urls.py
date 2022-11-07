from django.conf import settings
from django.contrib.auth.views import LogoutView
from django.urls import path

from .views import (dashboard_register, dashboard_login, dashboard_analytics, dashboard_products, dashboard_contact, \
                    edit_product, create_product, dashboard_orders, delete_product, VendorViews,
                    shop_update, create_shop)

urlpatterns = [
    # auth
    path("", dashboard_login, name="login"),
    path("register", dashboard_register, name="register"),
    path("create_shop", create_shop, name="create_shop"),
    path("logout/", LogoutView.as_view(), {'next_page': settings.LOGOUT_REDIRECT_URL}, name='logout'),
    
    # dashboard
    path("analytics", dashboard_analytics, name="analytics"),
    path("shop", shop_update, name="shop_update"),
    path("orders/<str:status>", dashboard_orders, name="vendor_orders"),
    # path("orders/<int:id>/manage", manage_orders, name="manage_orders"),
    path("products", dashboard_products, name="products"),
    path("products/create", create_product, name="create_product"),
    path("products/<int:id>/edit", edit_product, name="product_edit"),
    path("products/<int:id>/delete", delete_product, name="product_delete"),
    path("contact", dashboard_contact, name="contact"),

    # Vendor api for app
    path("vendors/", VendorViews.as_view(), name="vendor"),
]

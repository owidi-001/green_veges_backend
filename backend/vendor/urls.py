from django.urls import path

from .views import dashboard_login,dashboard_register,dashboard_analytics,dashboard_products

urlpatterns = [
    path("vendor/", dashboard_login, name="login"),
    path("vendor/create", dashboard_register, name="register"),
    path("vendor/analytics", dashboard_analytics, name="analytics"),
    path("vendor/products", dashboard_products, name="products"),
    # path("vendor/", VendorViews.as_view(), name="vendor"),
]

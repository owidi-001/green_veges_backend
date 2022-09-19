from django.urls import path

from product.views import ProductView,CategoryView


urlpatterns = [
    path("product/", ProductView.as_view(), name="product"),
    path("categories/", CategoryView.as_view(), name="product"),
]

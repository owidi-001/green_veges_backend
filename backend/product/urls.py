from django.urls import path

from product.views import ProductView

urlpatterns = [
    path("product/", ProductView, name="product"),
]

from django.urls import path

from product.views import ProductView

urlpatterns = [
    path("product/", ProductView.as_view(), name="product"),
]

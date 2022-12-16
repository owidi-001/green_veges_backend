from django.urls import path

from .views import CartView, CartItemView

urlpatterns = [
    path("", CartView().as_view(), name="orders"),
    # path("detail/", CartDetailView().as_view(), name="order_detail"),
    path("items", CartItemView().as_view(), name="items")
]

from django.conf import settings
from django.contrib.auth.views import LogoutView
from django.urls import path

from .views import OrderView, OrderItemView

urlpatterns = [
    # Auth user
    path("order", OrderView.as_view(), name="order"),
    path("order/item", OrderItemView.as_view(), name="order_item"),
]

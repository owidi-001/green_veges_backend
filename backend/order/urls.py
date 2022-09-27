from django.urls import path

from .views import OrderView, OrderItemView, AddressView, FeedbackView

urlpatterns = [
    # Auth user
    path("order", OrderView.as_view(), name="order"),
    path("order/item", OrderItemView.as_view(), name="order_item"),
    path("address", AddressView.as_view(), name="address"),
    path("feedback", FeedbackView.as_view(), name="feedback"),
]

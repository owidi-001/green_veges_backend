from django.urls import path

from .views import OrderView, OrderItemView, AddressView, FeedbackView

urlpatterns = [
    # Auth user
    path("orders", OrderView.as_view(), name="orders"),
    path("order_items", OrderItemView.as_view(), name="order_items"),
    path("address", AddressView.as_view(), name="address"),
    path("feedback", FeedbackView.as_view(), name="feedback"),
]

from django.urls import path

from .views import OrderView, OrderItemView

urlpatterns = [
    path("", OrderView().as_view(), name="orders"),
    path("items/", OrderItemView().as_view(), name="items")
]

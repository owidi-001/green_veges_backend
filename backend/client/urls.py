from django.urls import path

from client.views import ProductListView

urlpatterns = [
    path('clients/', ProductListView.as_view(), name="client")
]

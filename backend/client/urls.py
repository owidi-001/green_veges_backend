from django.urls import path

from .views import ClientProfileView

urlpatterns = [
    path('clients/', ClientProfileView.as_view(), name="client")
]

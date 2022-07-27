from django.urls import path

from .views import VendorViews

urlpatterns=[
    path("vendor/",VendorViews.as_view(),name="vendor")
]
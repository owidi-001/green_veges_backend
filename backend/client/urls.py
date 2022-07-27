from django.urls import path

from .views import ClientPageView

urlpatterns=[
    path('clients/',ClientPageView.as_view(),name="client")
]
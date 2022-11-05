from django.urls import path
from . import views

urlpatterns = [
    path('payment', views.MpesaPaymentView.as_view(), name='payment'),
    path('confirmation', views.MpesaConfirmationView.as_view(), name='confirmation'),
]

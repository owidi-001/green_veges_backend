from django.urls import path
from . import views

urlpatterns = [
    path('payment', views.MpesaPaymentView.as_view(), name='payment'),
    path('confirmation', views.MpesaConfirmationView.as_view(), name='confirmation'),

    # path('confirmation', views.confirmation, name="confirmation"),
    # path('access/token', views.getAccessToken, name='get_mpesa_access_token'),
    # # register, confirmation, validation and callback urls
    # path('c2b/register', views.register_urls, name="register_mpesa_validation"),
    # path('c2b/validation', views.validation, name="validation"),
    # path('c2b/callback', views.call_back, name="call_back"),
]

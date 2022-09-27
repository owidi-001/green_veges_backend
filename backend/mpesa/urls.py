from django.urls import path
from . import views

urlpatterns = [
    path('access/token', views.getAccessToken, name='get_mpesa_access_token'),
    # path('pay', views.lipa_na_mpesa_online, name='lipa_na_mpesa'),
    path('pay', views.MpesaView.as_view(), name='lipa_na_mpesa'),

    # register, confirmation, validation and callback urls
    path('c2b/register', views.register_urls, name="register_mpesa_validation"),
    path('c2b/confirmation', views.confirmation, name="confirmation"),
    path('c2b/validation', views.validation, name="validation"),
    path('c2b/callback', views.call_back, name="call_back"),
]

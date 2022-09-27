from django.utils.decorators import method_decorator
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from django.http import HttpResponse, JsonResponse
import requests
from requests.auth import HTTPBasicAuth
import json
from django.views.decorators.csrf import csrf_exempt
from .models import MpesaPayment

from .mpesa_config import MpesaConfig as config
from .mpesa_credentials import MpesaAccessToken, LipanaMpesaPpassword

BASE_URL = ""  # Ngrok server:port # Change to courier heroku: Basic Idea is it can't run locally


# shipment
@method_decorator(csrf_exempt, name="dispatch")
class MpesaView(APIView):
    # Protect view to only the authenticated
    permission_classes = (IsAuthenticated,)

    """
    Returns all user shipments 
    """

    def get(self,request):
        user = request.user
        phone = user.phone_number.split("+")[1]
        # phone=254791381653
        access_token = MpesaAccessToken.validated_mpesa_access_token
        api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
        headers = {"Authorization": "Bearer %s" % access_token}
        request = {
            "BusinessShortCode": LipanaMpesaPpassword.Business_short_code,
            "Password": LipanaMpesaPpassword.decode_password,
            "Timestamp": LipanaMpesaPpassword.lipa_time,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": 1,
            # "PartyA": 254791381653,  # replace with your phone number to get stk push
            "PartyA": phone,  # replace with your phone number to get stk push
            "PartyB": LipanaMpesaPpassword.Business_short_code,
            "PhoneNumber": phone,  # replace with your phone number to get stk push
            "CallBackURL": "https://sandbox.safaricom.co.ke/mpesa/",
            "AccountReference": "Courier",
            "TransactionDesc": "Payment for shipment"
        }
        response = requests.post(api_url, json=request, headers=headers)
        return HttpResponse('success')


def getAccessToken(request):
    consumer_key = config.CONSUMER_KEY
    consumer_secret = config.CONSUMER_SECRET
    api_URL = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'

    response = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    mpesa_access_token = json.loads(response.text)
    validated_mpesa_access_token = mpesa_access_token['access_token']
    return HttpResponse(validated_mpesa_access_token)

# @login_required
# def lipa_na_mpesa_online(request):
#     user = request.user
#     phone = user.phone_number.split("+")[1]
#     # phone=254791381653
#     access_token = MpesaAccessToken.validated_mpesa_access_token
#     api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
#     headers = {"Authorization": "Bearer %s" % access_token}
#     request = {
#         "BusinessShortCode": LipanaMpesaPpassword.Business_short_code,
#         "Password": LipanaMpesaPpassword.decode_password,
#         "Timestamp": LipanaMpesaPpassword.lipa_time,
#         "TransactionType": "CustomerPayBillOnline",
#         "Amount": 1,
#         # "PartyA": 254791381653,  # replace with your phone number to get stk push
#         "PartyA": phone,  # replace with your phone number to get stk push
#         "PartyB": LipanaMpesaPpassword.Business_short_code,
#         "PhoneNumber": phone,  # replace with your phone number to get stk push
#         "CallBackURL": "https://sandbox.safaricom.co.ke/mpesa/",
#         "AccountReference": "Courier",
#         "TransactionDesc": "Payment for shipment"
#     }
#     response = requests.post(api_url, json=request, headers=headers)
#     return HttpResponse('success')


@csrf_exempt
def register_urls(request):
    access_token = MpesaAccessToken.validated_mpesa_access_token
    api_url = "https://sandbox.safaricom.co.ke/mpesa/c2b/v1/registerurl"
    headers = {"Authorization": "Bearer %s" % access_token}
    options = {"ShortCode": LipanaMpesaPpassword.Business_short_code,
               "ResponseType": "Completed",
               "ConfirmationURL": f"{BASE_URL}/c2b/confirmation",
               "ValidationURL": f"{BASE_URL}/c2b/validation"}
    response = requests.post(api_url, json=options, headers=headers)
    return HttpResponse(response.text)


@csrf_exempt
def call_back(request):
    pass


@csrf_exempt
def validation(request):
    context = {
        "ResultCode": 0,
        "ResultDesc": "Accepted"
    }
    return JsonResponse(dict(context))


@csrf_exempt
def confirmation(request):
    mpesa_body = request.body.decode('utf-8')
    mpesa_payment = json.loads(mpesa_body)
    payment = MpesaPayment(
        first_name=mpesa_payment['FirstName'],
        last_name=mpesa_payment['LastName'],
        middle_name=mpesa_payment['MiddleName'],
        description=mpesa_payment['TransID'],
        phone_number=mpesa_payment['MSISDN'],
        amount=mpesa_payment['TransAmount'],
        reference=mpesa_payment['BillRefNumber'],
        organization_balance=mpesa_payment['OrgAccountBalance'],
        type=mpesa_payment['TransactionType'],
    )
    payment.save()
    context = {
        "ResultCode": 0,
        "ResultDesc": "Accepted"
    }
    return JsonResponse(dict(context))

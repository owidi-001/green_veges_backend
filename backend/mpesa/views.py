import json
import datetime
import requests
from coreapi.auth import TokenAuthentication
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from requests.auth import HTTPBasicAuth
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Payment
from .mpesa_config import MpesaConfig as config
from .mpesa_credentials import MpesaAccessToken, LipanaMpesaPassword
from .serializers import PaymentSerializer
from .utils import format_response, validate_phone, reformat_phone
from user.models import User

SERVER_URL = config.SERVER_URL
SANDBOX_URL = config.SANDBOX_URL


@method_decorator(csrf_exempt, name="dispatch")
class MpesaPaymentView(APIView):
    """
    Processes payment request by sending stk push to the given phone number
    """
    # authentication_classes = [TokenAuthentication]
    permission_classes = [AllowAny]

    def post(self, request):
        # Mpesa acceptable numbers begin with 254
        if not request.data["phone"]:
            phone = validate_phone(request.user.phone_number)
        else:
            phone = validate_phone(request.data["phone"])

        # phone = "254791381653"
        access_token = MpesaAccessToken.validated_mpesa_access_token

        api_url = f"{SANDBOX_URL}stkpush/v1/processrequest"

        headers = {"Authorization": "Bearer %s" % access_token}

        request = {
            "BusinessShortCode": LipanaMpesaPassword.Business_short_code,
            "Password": LipanaMpesaPassword.decode_password,
            "Timestamp": LipanaMpesaPassword.lipa_time,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": 1,
            "PartyA": phone,
            "PartyB": LipanaMpesaPassword.Business_short_code,
            "PhoneNumber": phone,
            # "CallBackURL": f"{SERVER_URL}mpesa/confirmation",
            "CallBackURL": "https://0e82-41-89-96-9.in.ngrok.io/mpesa/confirmation",
            "AccountReference": "Meal-io",
            "TransactionDesc": "Pay for your meal order"
        }

        response = requests.post(api_url, json=request, headers=headers)

        if response.status_code == status.HTTP_200_OK:
            return Response(response.text, status=status.HTTP_200_OK)
        print(response.text)
        return Response(response.text, status == response.status_code)


class MpesaConfirmationView(APIView):
    """
    Receives mpesa payment response and if valid, saved it to the database
    """

    def get(self, request):

        return Response(request.body)

    @csrf_exempt
    def post(self, request):
        # print(request.body)
        mpesa_body = request.body.decode('utf-8')
        data = format_response(json.loads(mpesa_body))

        # Fetch user with the phone number used for payment
        user = get_object_or_404(User, phone_number=reformat_phone(str(data["PhoneNumber"])))

        payment = Payment.objects.create(
            user=user,
            amount=data["Amount"],
            mpesaReceiptNumber=data["MpesaReceiptNumber"],
            balance=data["Balance"],
            transactionDate=datetime.datetime.utcfromtimestamp(int(data["TransactionDate"]) / 1000).strftime(
                '%d-%m-%Y %H:%M'),
            phone=data["PhoneNumber"]
        )

        # print(payment)
        payment.save()

        serializer = PaymentSerializer(payment)
        # print("payment saved")
        return Response(serializer.data, status=status.HTTP_201_CREATED)

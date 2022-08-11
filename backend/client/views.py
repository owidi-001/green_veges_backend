# Create your views here.
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from product.models import Product
from product.serializer import ProductSerializer
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from rest_framework.response import Response
from rest_framework.views import APIView

from client.client_schema import ClientSchema
from client.models import Client
from client.forms import ClientProfileUpdateForm
from client.serializer import ClientSerializer

from user.models import User


@method_decorator(csrf_exempt, name="dispatch")
class ClientProfileView(APIView):
    """
    Returns the basic saved customer details such as email,username, phone and orders.
    """

    schema = ClientSchema()

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def client_active(self, request):
        """
        Activate client when he or she has made at least one shipment
        """
        client = get_object_or_404(Client, user=request.user)
        # orders = ClientOrders.objects.filter(customer=client.user)

        # if len(orders) > 0 and not client.is_active:
        #     client.is_active = True
        #     client.save()

        return client

    def get(self, request):
        """
        Returns user profile
        """
        client = self.client_active(request)

        response = ClientSerializer(client).data
        return Response(response, status=200)

    def put(self, request):
        """update profile - email, phone number"""
        form = ClientProfileUpdateForm(request.data)

        if form.is_valid():
            user = get_object_or_404(User, username=request.user.username)

            print("client retrieved", user.email)

            if form.cleaned_data.get("first_name"):
                print(form.cleaned_data.get("first_name"))
                user.first_name = form.cleaned_data["first_name"]
                user.save()

            if form.cleaned_data.get("last_name"):
                print(form.cleaned_data.get("last_name"))
                user.last_name = form.cleaned_data["last_name"]
                user.save()

            if form.cleaned_data.get("email"):
                print(form.cleaned_data.get("email"))
                user.email = form.cleaned_data["email"]
                user.save()

            if form.cleaned_data.get("phone_number"):
                user.phone_number = form.cleaned_data["phone_number"]
                user.save()

            client = get_object_or_404(Client, user=user)

            try:
                client.save()
                print("Client saved")

            except:
                print(client)
            return Response(ClientSerializer(client).data, status=status.HTTP_200_OK)
        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductListView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    """
        Product list of available products
    """

    def get(self, request):
        """
        List of all available products
        """
        query = Product.objects.all()

        return Response(
            ProductSerializer(query, many=True).data, status=status.HTTP_200_OK
        )
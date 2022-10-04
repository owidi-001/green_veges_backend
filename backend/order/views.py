from threading import Thread

from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from order.forms import AddressForm, FeedbackForm, OrderItemForm, OrderItemUpdateForm, \
    OrderForm, OrderUpdateForm
from order.models import Address
from order.models import Order, OrderItem
from order.schema import AddressSchema, OrderItemSchema, OrderSchema, FeedbackSchema
from order.serializers import FeedbackSerializer, AddressSerializer
from order.serializers import OrderSerializer, OrderItemSerializer
from product.models import Product
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
# Create your views here.
from rest_framework.views import APIView


class EmailThead(Thread):
    def __init__(self, email_to, message, subject):
        super().__init__()
        self.email_to = email_to
        self.message = message
        self.subject = subject

    def run(self):
        send_mail(message=self.message, recipient_list=self.email_to, subject=self.subject)


@method_decorator(csrf_exempt, name='dispatch')
class OrderView(APIView):
    """
    Orders operations for the client user
    """
    schema = OrderSchema()
    authentication_classes = [TokenAuthentication]
    permission_classes = [AllowAny]

    def get(self, request):
        user = request.user
        orders = Order.objects.filter(customer=user)

        if user:
            data = OrderSerializer(orders, many=True).data

            return Response(data, status=200)
        return Response({"errors": ["orders not loaded"]}, status=400)

    def post(self, request):
        form = OrderForm(request.data)

        if form.is_valid():
            order = form.save(commit=False)
            order.customer = request.user
            order.save()

            email_to = request.user.email
            subject = "Order receipt confirmation"
            message = "Your order has been received. Processing is underway"

            # Mail the user confirming the order has been received
            EmailThead([email_to], message, subject).start()

            data = OrderSerializer(order).data
            return Response(data, status=200)
        return Response({"errors": ["Failed to create place order"]}, status=400)

    def put(self, request):
        form = OrderUpdateForm(request.data)

        if form.is_valid():
            print(form.cleaned_data.get("id"))
            order = get_object_or_404(Order, id=form.cleaned_data.get("id"))
            order.status = form.cleaned_data.get("status")
            order.save()

            email_to = request.user.email

            data = OrderSerializer(order).data

            if order.status == "F":

                subject = "Orders status"
                message = "Your orders have been successfully delivered. Thank you for shopping with us."

            elif order.status == "C":
                subject = "Order status"
                message = "Your order has been cancelled."
            else:
                subject = "Order status"
                message = "Your order processed awaiting transport"

            # Mail the user confirming the order has been fulfilled
            EmailThead([email_to], message, subject).start()
            return Response(data, status=200)

        return Response({"errors": ["Failed to update order"]}, status=400)

    def delete(self, request):
        form = OrderUpdateForm(request.data)
        if form.is_valid():
            order = get_object_or_404(Order, id=form.cleaned_data.get("order_id"))

            if order:
                order.delete()
                return Response({"message": "Deletion successful"}, status=200)
        return Response({"errors": ["Failed to deletion"]}, status=400)


@method_decorator(csrf_exempt, name='dispatch')
class OrderItemView(APIView):
    """
    Order items operations for the client user
    """
    schema = OrderItemSchema()

    authentication_classes = [TokenAuthentication]
    permission_classes = [AllowAny]

    def get(self, request):
        orders = Order.objects.filter(customer=request.user)

        items = []
        for order in orders:
            order_items = OrderItem.objects.filter(order=order)
            items += order_items

        data = OrderItemSerializer(items, many=True).data

        return Response(data, status=200)

    # Create new order item
    def post(self, request):
        form = OrderItemForm(request.data)
        if form.is_valid():
            order = form.cleaned_data.get("order")
            product = form.cleaned_data.get("product")
            quantity = form.cleaned_data.get("quantity")

            product = get_object_or_404(Product, id=product)
            order = get_object_or_404(Order, id=order)

            order_item = OrderItem.objects.create(order=order, product=product, quantity=quantity)
            if order_item:
                order_item.save()
                data = OrderItemSerializer(order_item).data
                return Response(data, status=200)
        print(form.errors)
        return Response({"errors": ["Failed to create place order"]}, status=400)

    # Update order when payment is done
    def put(self, request):
        form = OrderItemUpdateForm(request.data)

        if form.is_valid():
            order_item = get_object_or_404(OrderItem, id=request.order_item)

            order_item.status = form.cleaned_data.get("status")
            order_item.save()
            data = OrderItemSerializer(order_item).data

            return Response(data, status=200)
        return Response({"errors": ["Failed to update order item"]}, status=400)


@method_decorator(csrf_exempt, name='dispatch')
class AddressView(APIView):
    """
    Create, retrieve and delete user address
    """
    schema = AddressSchema()

    authentication_classes = [TokenAuthentication]
    permission_classes = [AllowAny]

    """
    Retrieve saved user addresses
    """

    def get(self, request):
        addresses = Address.objects.filter(user=request.user)
        data = AddressSerializer(addresses, many=True).data
        return Response(data, status=200)

    def post(self, request):
        form = AddressForm(request.data)

        if form.is_valid():
            print("Form is valid")
            address = form.save(commit=False)
            address.user = request.user

            address.save()

            data = AddressSerializer(address).data

            return Response(data, status=200)
        print(f"Form is not valid{form.errors}")
        return Response({"errors": ["Failed to create address"]}, status=400)

    def delete(self, request):
        address_id = request.id
        address = get_object_or_404(Address, id=address_id)

        if address:
            address.delete()
            return Response({"message": ["Deleted successfully"]}, status=200)
        else:
            return Response({"errors": ["Failed to delete"]}, status=400)


@method_decorator(csrf_exempt, name='dispatch')
class FeedbackView(APIView):
    """
    Client gives feedback on order
    """
    schema = FeedbackSchema()
    authentication_classes = [TokenAuthentication]
    permission_classes = [AllowAny]

    # Create new order item
    def post(self, request):
        form = FeedbackForm(request.data)

        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.user = request.user
            feedback.save()

            data = FeedbackSerializer(feedback).data

            return Response(data, status=200)
        return Response({"errors": ["Failed to create feedback"]}, status=400)

from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from order.models import Order, OrderItem
from order.serializers import OrderSerializer, OrderItemSerializer
from product.models import Product
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
# Create your views here.
from rest_framework.views import APIView
from user.models import User, EmailThead


@method_decorator(csrf_exempt, name='dispatch')
class OrderView(APIView):
    """
    Orders operations for the client user
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = get_object_or_404(User, user=request.user)
        orders = Order.objects.filter(customer=user)

        if user:
            data = OrderSerializer(orders, many=True).data

            return Response(data, status=200)
        return Response({"errors": ["orders not loaded"]}, status=400)

    # Create new order
    def post(self, request):
        customer = request.user
        total = request.total
        delivery_address = request.address

        order = Order.objects.create(customer=customer, total=total, delivery_address=delivery_address)
        if order:
            order.save()
            email_to = customer.email
            subject = "Order receipt confirmation"
            message = "Your order has been received"

            # Mail the user confirming the order has been received
            EmailThead([email_to], message, subject).start()

            data = OrderSerializer(order).data
            return Response(data, status=200)
        return Response({"errors": ["Failed to create place order"]}, status=400)

    # Update order when payment is done
    def put(self, request):
        order = get_object_or_404(Order, id=request.order)

        if order:
            order_status = request.status
            order.status = order_status
            order.save()
            data = OrderSerializer(order).data
            return Response(data, status=200)
        return Response({"errors": ["Failed to update order"]}, status=400)

    # delete
    def delete(self, request):
        order = get_object_or_404(Order, id=request.order)

        if order:
            order.delete()
            return Response({"message": "Deletion successful"}, status=200)
        return Response({"errors": ["Failed to deletion"]}, status=400)

    def patch(self, request):
        order = get_object_or_404(Order, id=request.order)
        order_items = OrderItem.objects.filter(order=order)
        items_status = [item.status for item in order_items]
        if len(items_status) > 0:
            # All order items status are equal and fulfilled
            if len(set(items_status)) == 1 and items_status[0] == "F":
                order.status = "F"
                order.save()

                email_to = request.user.email
                subject = "Orders fulfilment"
                message = "Your orders have been successfully delivered. Thank you for shopping with us."

                # Mail the user confirming the order has been fulfilled
                EmailThead([email_to], message, subject).start()

                return Response({"message": "Order complete"}, status=200)


# order item view
@method_decorator(csrf_exempt, name='dispatch')
class OrderItemView(APIView):
    """
    Order items operations for the client user
    """

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        order_item = get_object_or_404(OrderItem, id=request.order_item)
        if order_item:
            data = OrderItemSerializer(order_item).data

            return Response(data, status=200)
        return Response({"errors": ["order item not loaded"]}, status=400)

    # Create new order item
    def post(self, request):
        order = get_object_or_404(Order, id=request.order)
        product = get_object_or_404(Product, id=request.product)
        quantity = request.quantity

        order_item = OrderItem.objects.create(order=order, product=product, quantity=quantity)

        if order_item:
            order_item.save()

            data = OrderItemSerializer(order_item).data
            return Response(data, status=200)
        return Response({"errors": ["Failed to create place order"]}, status=400)

    # Update order when payment is done
    def put(self, request):
        order_item = get_object_or_404(OrderItem, id=request.order_item)

        if order_item:
            order_status = request.status
            order_item.status = order_status
            order_item.save()
            data = OrderItemSerializer(order_item).data

            return Response(data, status=200)
        return Response({"errors": ["Failed to update order item"]}, status=400)
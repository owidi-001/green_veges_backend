# Create your views here.
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Cart, CartItem, Location
# from .schema import OrderSchema
from .schema import CartSchema, CartDetailSchema
from .serializers import CartItemSerializer, CartSerializer, CartDetailSerializer
from product.models import Product


class CartView(APIView):
    """
    Cart list, post and put views
    """
    schema = CartSchema()
    authentication_classes = [TokenAuthentication]
    permission_classes = [AllowAny]

    def get(self, request):
        orders = Cart.objects.all()
        # print(orders)
        serializer = CartSerializer(orders, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data

        # See the nature of request data
        print(data)

        payment_done = True

        # Create objects from the request data
        location = Location.objects.get_or_create(name=data["location"]["name"],
                                                  block_name=data["location"]["block_name"],
                                                  floor_number=data["location"]["floor_number"],
                                                  room_number=data["location"]["room_number"]
                                                  )

        # Create order object
        cart = Cart.objects.create(user=request.user, location=location[0], total=data["total"])

        if cart:
            cart.save()

            # Save cart items
            items = data["items"]

            for item in items:
                product = get_object_or_404(Product, id=item["product"])
                CartItem.objects.create(cart=cart, product=product, quantity=item["quantity"]).save()
                print("Order item saved")

            # Trigger payment
            serializer = CartSerializer(cart)

            if payment_done:
                print("Everything successful")
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({"message": "Error creating the order"}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        data = request.data
        order = get_object_or_404(Cart, id=data["order"])

        # Check if data has location
        if data["location"]:
            name = data["location"]["name"]
            block_name = data["location"]["block_name"]
            floor_number = data["location"]["floor_number"]
            room_number = data["location"]["room_number"]

            location = Location.objects.update_or_create(name=name, block_name=block_name, floor_number=floor_number,
                                                         room_number=room_number)

            # The above returns a tuple of two, the object and bool if created
            # print(location)

            if location:
                order.location = location[0]
            else:
                print(location)

        if order:
            order.status = data["status"]
            order.save()
            return Response(status=status.HTTP_202_ACCEPTED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        data = request.data
        order = get_object_or_404(Cart, id=data["order"])

        if order:
            order.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class CartItemView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [AllowAny]

    def get(self, request):
        items = CartItem.objects.all()
        serializer = CartItemSerializer(items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        cart = get_object_or_404(Cart, id=data["cart"])
        product = get_object_or_404(Product, id=data["product"])
        quantity = data["quantity"]
        item = CartItem.objects.create(cart=cart, product=product, quantity=quantity)

        try:
            item.save()
            return Response(status=status.HTTP_201_CREATED)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        data = request.data
        item = get_object_or_404(CartItem, id=data["item"])

        if item:
            item.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)

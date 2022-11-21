# Create your views here.
from django.shortcuts import get_object_or_404
from product.models import Product
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Cart, CartItem, Location
# from .schema import OrderSchema
from .schema import CartSchema
from .serializers import CartItemSerializer, CartSerializer


class CartView(APIView):
    """
    Cart list, post and put views
    """
    schema = CartSchema()
    authentication_classes = [TokenAuthentication]
    permission_classes = [AllowAny]

    def get(self, request):
        orders = Cart.objects.all().order_by("-date_ordered")
        # print(orders)
        serializer = CartSerializer(orders, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    """
    Saves order once the payment is complete
    """

    def post(self, request):
        print("The cart order service accessed")
        data = request.data
        print(data)
        location = data["location"]
        delivery_location = Location.objects.get_or_create(name=location["name"],
                                                           block_name=location["block_name"],
                                                           floor_number=location["floor_number"],
                                                           room_number=location["room_number"]
                                                           )

        # Create order object
        cart = Cart.objects.create(user=request.user, location=delivery_location[0], total=data["total"])

        if cart:
            cart.save()
            print("cart saved")
            # Save cart items
            items = data["items"]

            for item in items:
                product = get_object_or_404(Product, id=item["product"])
                if product:
                    CartItem.objects.create(cart=cart, product=product, quantity=item["quantity"]).save()
                    product.stock -= item["quantity"]
                    product.save()
                # print("Order item saved")

            # Trigger payment
            serializer = CartSerializer(cart)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({"message": "Error creating the order"}, status=status.HTTP_400_BAD_REQUEST)


    def put(self, request):
        data = request.data
        print(data)
        order = get_object_or_404(CartItem, id=data["order"])

        # Check if data has location
        try:
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
        except:
            pass

        if order:
            order.status = data["status"]
            order.save()
            print("Order saved")
            
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

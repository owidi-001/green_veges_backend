from rest_framework import serializers

from .models import Cart, CartItem
from product.serializer import ProductSerializer


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = CartItem
        fields = ["id", "cart", "quantity", "product"]


class CartSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cart
        fields = ["user", "status", "date_ordered", "location"]

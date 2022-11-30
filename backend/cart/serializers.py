from product.serializer import ProductSerializer
from rest_framework import serializers

from .models import Cart, CartItem, Location


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ["id","name", "block_name", "floor_number", "room_number"]


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = CartItem
        fields = ["id", "cart", "quantity", "product","status"]


class CartSerializer(serializers.ModelSerializer):
    location = LocationSerializer(read_only=True)

    class Meta:
        model = Cart
        fields = ["id", "user", "status", "total", "date_ordered", "location"]


class CartDetailSerializer(serializers.ModelSerializer):
    location = LocationSerializer(read_only=True)
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ["id", "user", "status", "total", "date_ordered", "location", "items"]

from rest_framework import serializers
from rider.models import OrderRider, Rider
from cart.serializers import CartItemSerializer



class RiderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rider
        fields = ["id", "user", "license"]


class CartItemRiderSerializer(serializers.ModelSerializer):
    order = CartItemSerializer()
    rider = RiderSerializer()

    class Meta:
        model = OrderRider
        fields = ["id", "rider", "order"]


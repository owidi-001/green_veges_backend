from rest_framework import serializers
from rider.models import OrderRider, Rider
from cart.serializers import CartItemSerializer, LocationSerializer



class RiderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rider
        fields = ["id", "user","brand","dob","national_id","license"]


class CartItemRiderSerializer(serializers.ModelSerializer):
    rider = RiderSerializer()
    item = CartItemSerializer()
    location=LocationSerializer()

    class Meta:
        model = OrderRider
        fields = ["id", "rider", "item","location"]


from rest_framework import serializers

from .models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment # return true since payment saved is success
        fields = ["user","phone","amount","mpesaReceiptNumber"]

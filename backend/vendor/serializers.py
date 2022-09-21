# USERS and AUTH
from rest_framework import serializers

from vendor.models import Vendor


class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ["user", "brand", "tagline", "logo"]

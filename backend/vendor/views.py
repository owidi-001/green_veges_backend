from django.shortcuts import get_object_or_404
from product.forms import ProductForm
from product.forms import ProductUpdateForm
from product.models import Product
from product.schema import ProductSchema
from product.serializer import ProductSerializer
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from vendor.models import Vendor


class VendorViews(APIView):
    """ Vendor dashboard functions: list, create, update, delete for products"""

    schema = ProductSchema()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    """ Gets a list of all products belonging to the vendor """

    def get(self, request):
        vendor = get_object_or_404(Vendor, user=request.user)
        products = Product.objects.filter(vendor=vendor)

        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
from django.shortcuts import get_object_or_404, redirect, render
# from django.utils.decorators import method_decorator
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .forms import ProductUpdateForm
from .models import Product
from .schema import ProductSchema
from .serializer import ProductSerializer

# class views
from vendor.models import Vendor


class ProductView(APIView):
    """
    List all products and CRUD operations for detail view for the product
    """

    schema = ProductSchema()
    #
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    """ Returns all available products """

    def get(self, request):
        vendor = get_object_or_404(Vendor, user=request.user)
        if vendor:
            products = Product.objects.filter(vendor=vendor)
        else:
            products = Product.objects.all()

        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    def put(self, request):
        form = ProductUpdateForm(request.data)

        if form.is_valid():
            product = get_object_or_404(Product, id=request.data.get("product_id"))

            if form.cleaned_data.get("label"):
                product.label = form.cleaned_data.get("label")

            if form.cleaned_data.get("price"):
                product.unit_price = form.cleaned_data.get("price")

            if form.cleaned_data.get("description"):
                product.description = form.cleaned_data.get("description")

            if form.cleaned_data.get("quantity"):
                product.quantity = form.cleaned_data.get("quantity")

            product.save()

            serializer = ProductSerializer(product)

            return Response(serializer)
        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

    """ Vendor deletes a product from db """

    def delete(self, request):
        product = get_object_or_404(Product, pk=request.data.get("product_id"))
        vendor = request.user

        if product.vendor == vendor:
            product.delete()

            return Response({"message": "Product deleted"})
        else:
            return Response({"message": "Only the vendor can delete this product"})

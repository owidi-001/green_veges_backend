from django.shortcuts import get_object_or_404, redirect, render
# from django.utils.decorators import method_decorator
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .forms import ProductForm
from .models import Product, Category
from .schema import ProductSchema
from .serializer import ProductSerializer, CategorySerializer

# class views


class ProductView(APIView):
    """
    List all products and CRUD operations for detail view for the product
    """

    schema = ProductSchema()
    # permissions
    authentication_classes = [TokenAuthentication]
    permission_classes = [AllowAny]

    """ Returns all available products """

    def get(self, request):
        products = Product.objects.all()

        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    def put(self, request):
        form = ProductForm(request.data)

        if form.is_valid():
            product = get_object_or_404(Product, id=request.data.get("product_id"))

            if form.cleaned_data.get("label"):
                product.label = form.cleaned_data.get("label")

            if form.cleaned_data.get("price"):
                product.unit_price = form.cleaned_data.get("price")

            if form.cleaned_data.get("description"):
                product.description = form.cleaned_data.get("description")

            if form.cleaned_data.get("stock"):
                product.stock = form.cleaned_data.get("stock")

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


class CategoryView(APIView):
    """
    List all categories
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [AllowAny]

    """ Returns all available categories """

    def get(self, request):
        categories = Category.objects.all()

        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

from django.shortcuts import get_object_or_404, render
from rest_framework.response import Response

from rest_framework.views import APIView


from user.models import User
from product.models import Product
from product.serializer import ProductSerializer

# Create your views here.
class VendorViews(APIView):
    """ Vendor dashboard functions: list, create, update, delete"""

    """ Gets a list of all products belonging to the vendor """
    def get(self,request):
        vendor=get_object_or_404(User,pk=request.user.id)
        products=Product.objects.filter(vendor=vendor)

        serializer=ProductSerializer(products,many=True)
        return Response(serializer.data)

    """ Adds new product to the database """
    def post(self,request):
        serializer=ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            return Response(serializer)

    """ Vendor Updates existing product"""
    def put(self,request):
        product=get_object_or_404(Product,pk=request.get("product_id"))

        serializer=ProductSerializer(data=request.data)

        if serializer.is_valid():
            if request.data.get("name"):
                product.name=request.data.get("name")

            if request.data.get("price"):
                product.price=request.data.get("price")

            if request.data.get("description"):
                product.description=request.data.get("description")

            product.save()                

            return Response(serializer)

    """ Vendor deletes a product from db """
    def delete(self,request):
        product=get_object_or_404(Product,pk=request.get("product_id"))
        vendor=request.user

        if product.vendor==vendor:
            product.delete()

            return Response({"message":"Product deleted"})

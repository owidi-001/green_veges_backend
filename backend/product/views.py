from django.shortcuts import get_object_or_404
# from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from .schema import ProductSchema
from .models import Product
from .serializer import ProductSerializer


# class views
from vendor.models import Vendor


@csrf_exempt
class ProductView(APIView):
    """
    List all products and CRUD operations for detail view for the product
    """

    schema = ProductSchema()
    #
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    """ Returns all available products """

    def get(self):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    """ Creates new product to the database """

    def post(self, request):
        vendor = get_object_or_404(Vendor, user=request.user)
        serializer = ProductSerializer(data=request.data)

        if serializer.is_valid():
            product = serializer.save()
            return Response(product, status=201)

        return Response(serializer.errors, status=400)

    """ Updates an existing product price, description and label"""

    def put(self, request):
        product = self.get_product(request)

        if product:
            if request.data.get("label"):
                product.label = request.data.get("label")
            if request.data.get("price"):
                product.price = request.data.get("price")
            if request.data.get("description"):
                product.description = request.data.get("description")

        serializer = ProductSerializer(data=product)
        if serializer.is_valid():
            product = serializer.save()
            return Response(product, status=201)

        return Response(serializer.errors, status=400)

    """ Removes product from the database """

    def delete(self, request):
        product = self.get_product(request)

        if product:
            product.delete()
            return Response(status=200)

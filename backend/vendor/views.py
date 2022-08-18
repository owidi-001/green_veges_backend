from django.shortcuts import get_object_or_404, render
from product.models import Product
from product.schema import ProductSchema
from product.serializer import ProductSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from vendor.models import Vendor


# vendor dashboard
def dashboard_login(request):
    return render(request, "vendor/dashboard-login.html", {"title": "Vendor dashboard login"})


def dashboard_register(request):
    return render(request, "vendor/dashboard-register.html", {"title": "Vendor dashboard register"})


def dashboard_analytics(request):
    return render(request, "vendor/dashboard-analytics.html", {"title": "Vendor dashboard analytics"})


def dashboard_products(request):
    vendor = get_object_or_404(Vendor, user=request.user)
    products = Product.objects.filter(vendor=vendor)

    return render(request, "vendor/dashboard-products.html",
                  {"title": "Vendor dashboard product", "products": products})


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

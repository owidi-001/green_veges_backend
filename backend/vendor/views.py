from django.contrib.auth import authenticate, login
from django.shortcuts import get_object_or_404, render, redirect
from django.template.loader import render_to_string
from product.models import Product
from product.schema import ProductSchema
from product.serializer import ProductSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from user.forms import UserCreationForm
from user.serializers import UserSerializer
from user.views import EmailThead
from vendor.models import Vendor

# signup COMPLETE
from user.forms import UserLoginForm


def dashboard_register(request):
    form = UserCreationForm(request.POST)
    # if not form.is_valid():
    #     print(form.errors)

    if request.method == 'POST' and form.is_valid():
        user = form.save()
        email_to = form.cleaned_data.get("email")
        print("Emailing to:", email_to)
        scheme = request.build_absolute_uri().split(":")[0]
        path = f"{scheme}://{request.get_host()}/login"
        print(path)
        message = render_to_string("registration_email.html", {
            "email": email_to, "path": path})
        subject = "Registration confirmation"

        EmailThead([email_to], message, subject).start()

        try:
            username = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password1")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
            return redirect("analytics")
        except:
            return redirect('login')
    else:
        return render(request, "vendor/dashboard-register.html",
                      {"title": "Vendor dashboard register", "errors": form.errors})


def dashboard_login(request):
    form = UserLoginForm(request.POST or None)
    if request.POST and form.is_valid():
        username = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        print(username)
        print(password)
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('analytics')

    return render(request, "vendor/dashboard-login.html", {"title": "Vendor dashboard login"})


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

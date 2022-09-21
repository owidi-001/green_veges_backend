from json import dumps

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import get_object_or_404, render, redirect
from django.template.loader import render_to_string
from product.forms import ProductForm
from product.models import Category
from product.models import Product
from product.schema import ProductSchema
from product.serializer import ProductSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from user.forms import UserCreationForm
# signup COMPLETE
from user.forms import UserLoginForm
from user.models import User
from user.views import EmailThead
from vendor.forms import ContactForm
from vendor.models import Vendor

from order.models import Order

from order.models import OrderItem

from vendor.serializers import VendorSerializer


def dashboard_register(request):
    form = UserCreationForm(request.POST)
    if not form.is_valid():
        print(form.errors)

    if request.method == 'POST':
        if form.is_valid():
            user = form.save()
            email_to = form.cleaned_data.get("email")
            # print("Emailing to:", email_to)
            scheme = request.build_absolute_uri().split(":")[0]
            path = f"{scheme}://{request.get_host()}/login"
            # print(path)
            message = render_to_string("registration_email.html", {
                "email": email_to, "path": path})
            subject = "Registration confirmation"

            EmailThead([email_to], message, subject).start()

            try:
                username = form.cleaned_data.get("email")
                password = form.cleaned_data.get("password1")

                # Create vendor instance to login
                Vendor.objects.get_or_create(user=user)

                user = authenticate(username=username, password=password)

                print(f"user:{user}")

                if user:
                    login(request, user)
                    return redirect("analytics")
                else:
                    messages.info(request, "Account created, login to start")
                    return redirect('login')
            except:
                print("User not authenticated")
                messages.info(request, "Login failed")
                pass

        else:
            messages.error(request, form.errors)
            return render(request, "vendor/dashboard-register.html",
                          {"title": "Vendor dashboard register", "errors": form.errors})
    return render(request, "vendor/dashboard-register.html",
                  {"title": "Vendor dashboard register"})


def dashboard_login(request):
    form = UserLoginForm(request.POST or None)
    if request.POST and form.is_valid():
        username = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        # print(username)
        # print(password)
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('analytics')

    return render(request, "vendor/dashboard-login.html", {"title": "Vendor dashboard login"})


# def dashboard_logout(request):
#     active_users = User.objects.filter(is_active=True).count()
#     return render(request, "vendor/dashboard-analytics.html",
#                   {"title": "Vendor dashboard analytics", "active_users": active_users})
#

def formulate_daily_sales() -> list:
    pass


def dashboard_analytics(request):
    vendor = get_object_or_404(Vendor, user=request.user)
    active_users = User.objects.filter(is_active=True).count()

    orders = 0  # Total orders
    order_stream = 0  # Order for last 30 days
    customers = 0
    items_sold = 0

    # for order in OrderItem.objects.all():
    #     if order.product.vendor == vendor:
    #         order_stream += 1

    chart_label = '% Totals'
    on_transit = 3
    cancelled = 4
    pending = 2
    completed = 9

    order_stats = [
        ['Order', chart_label],
        ['On Transit', on_transit],
        ['Cancelled', cancelled],
        ['Pending', pending],
        ['Completed', completed],
    ]
    order_stats = dumps(order_stats)

    daily_sales = [
        ['Day', 'Daily Sales'],
        ['2004', 1000],
        ['2005', 1170],
        ['2006', 660],
        ['2005', 1170],
        ['2006', 660],
        ['2007', 1030],
        ['2007', 1030],
        ['2007', 1030],
        ['2007', 1030],
    ]
    daily_sales = dumps(daily_sales)
    context = {"title": "Vendor dashboard analytics", "active_users": active_users, "order_stream": order_stream,
               "customers": customers, "items_sold": items_sold, "orders": orders, "order_stats": order_stats,
               "daily_sales": daily_sales}

    return render(request, "vendor/dashboard-analytics.html",
                  context)


def dashboard_products(request):
    vendor = get_object_or_404(Vendor, user=request.user)
    products = Product.objects.filter(vendor=vendor)

    return render(request, "vendor/dashboard-products.html",
                  {"title": "Vendor dashboard product", "products": products})


def dashboard_orders(request):
    vendor = get_object_or_404(Vendor, user=request.user)
    # order_items = OrderItem.objects.filter(product.vendor == vendor)
    order_items = OrderItem.objects.all()
    orders = []
    for order_item in order_items:
        if order_item.product.vendor == vendor:
            if order_item.order not in orders:
                orders.append(order_item.order)

    return render(request, "vendor/dashboard-orders.html",
                  {"title": "Vendor dashboard orders", "orders": orders})


def manage_orders(request, id):
    vendor = get_object_or_404(Vendor, user=request.user)
    order = get_object_or_404(Order, id=id)
    order_items = OrderItem.objects.filter(order=order)

    orders = []

    for order_item in order_items:
        if order_item.product.vendor == vendor:
            orders.append(order_item)

    return render(request, "vendor/manage-orders.html",
                  {"title": "Manage orders", "order_items": order_items})


# product create
def create_product(request):
    categories = Category.objects.all()
    form = ProductForm(request.POST, request.FILES)

    # print(request.POST)
    # print(request.FILES)

    if form.is_valid():
        product = form.save(commit=False)
        product.vendor = get_object_or_404(Vendor, user=request.user)
        product.save()
        messages.success(request, f"We have successfully added {product.label} to your list!")
        return redirect('products')
    else:
        messages.error(request, f"{form.errors}")

    return render(request, "vendor/product-create.html",
                  {"errors": form.errors, 'categories': categories, 'current_category': None})


# edit product
def edit_product(request, id):
    product = get_object_or_404(Product, id=id)
    form = ProductForm(request.POST, request.FILES)
    categories = Category.objects.all()

    print(request.POST)
    print(form.errors)

    if request.POST and form.is_valid():
        label = form.cleaned_data.get('label')
        unit_price = float(form.cleaned_data.get('unit_price'))
        quantity = int(form.cleaned_data.get('quantity'))
        image = form.cleaned_data.get("image")
        description = form.cleaned_data.get("description")
        category = request.POST['category']

        # print(category)
        product_category = get_object_or_404(Category, id=category)

        # Update product
        if label:
            product.label = label

        if unit_price:
            product.unit_price = unit_price

        if description:
            product.description = description

        if quantity:
            product.quantity = quantity

        if product_category:
            product.category = product_category

        if image:
            product.image = image

        product.save()
        messages.success(request, 'Your product has been updated successfully')
        return redirect('products')

    return render(request, "vendor/product-edit.html",
                  {'product': product, 'categories': categories, 'current_category': product.category,
                   "errors": form.errors})


# delete product
def delete_product(request, id):
    user = request.user
    vendor = get_object_or_404(Vendor, user=user)
    product = get_object_or_404(Product, id=id)
    if product.vendor == vendor:
        product.delete()
        messages.success(request, "Product deleted successfully")
        return redirect('products')
    messages.error(request, "The delete operation falied")
    return redirect('products')


def dashboard_contact(request):
    form = ContactForm(request.POST, request.FILES)
    vendor = get_object_or_404(Vendor, user=request.user)

    # print(form.errors)
    # print(request.POST)

    if request.POST and form.is_valid():
        contact = form.save(commit=False)
        contact.vendor = vendor

        if form.cleaned_data.get("email"):
            email = form.cleaned_data.get("email")
        else:
            email = vendor.user.email

        subject = form.cleaned_data.get("subject")
        message = form.cleaned_data.get("message")

        # Email the admin
        EmailThead([settings.EMAIL_HOST_USER, "kevinalex846@gmail.com"], message, subject).start()

        messages.info(request, "Your message has been received and you'll be contacted shortly")
        return redirect("analytics")
    return render(request, "vendor/dashboard-contact.html",
                  {"title": "Vendor dashboard contact"})


class VendorViews(APIView):
    """ Vendor dashboard functions: list, create, update, delete for products"""

    authentication_classes = [TokenAuthentication]
    permission_classes = [AllowAny]

    """ Gets a list of all products belonging to the vendor """

    def get(self, request):
        # vendor = get_object_or_404(Vendor, user=request.user)
        # products = Product.objects.filter(vendor=vendor)
        #
        # serializer = ProductSerializer(products, many=True)
        # return Response(serializer.data)
        vendors = Vendor.objects.all()
        serializer = VendorSerializer(vendors, many=True)
        return Response(serializer.data)

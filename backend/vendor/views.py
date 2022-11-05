import datetime
from json import dumps
from collections import defaultdict

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import get_object_or_404, render, redirect
from django.template.loader import render_to_string
from django.utils import timezone
from order.models import Order
from product.forms import ProductForm
from product.models import Category
from product.models import Product
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from user.forms import UserCreationForm
# signup COMPLETE
from user.forms import UserLoginForm
from user.models import User
from user.views import EmailThead
from vendor.forms import ContactForm
from vendor.models import Vendor
from vendor.serializers import VendorSerializer

from vendor.forms import ShopForm


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
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('analytics')
    else:
        print(form.errors)
    return render(request, "vendor/dashboard-login.html", {"title": "Vendor dashboard login"})


def dashboard_shop(request):
    vendor = get_object_or_404(Vendor, user=request.user)

    form = ShopForm(request.POST, request.FILES)

    if request.POST and form.is_valid():
        vendor.brand = form.cleaned_data.get("brand")

        print(form.cleaned_data.get("brand"))
        print(form.cleaned_data.get("tagline"))

        if form.cleaned_data.get("brand"):
            vendor.brand = form.cleaned_data.get("brand")
        if form.cleaned_data.get("tagline"):
            vendor.tagline = form.cleaned_data.get("tagline")
        if form.cleaned_data.get("logo"):
            vendor.logo = form.cleaned_data.get("logo")
        vendor.save()

        messages.info(request, "Your shop has been saved successfully")
        return redirect("analytics")
    print(form.errors)
    return render(request, "vendor/shop.html")


def formulate_daily_sales() -> list:
    """ Initialize daily sales """
    daily_sales = [
        ['Day', 'Daily Sales'],
    ]

    """Create sales date list"""
    sales_date = []
    for i in range(0, 10):
        sales_date.append(str((timezone.now() - datetime.timedelta(days=i)).date()))

    """ Calculate daily totals """
    # Vendors last 10 days sales
    vendor_recent_sales = OrderItem.objects.filter(timestamp__lt=timezone.now() - datetime.timedelta(days=10))

    # Daily sales grouping for the lists of items sold in a day
    # Group orderItems as per dates
    vendor_daily_sales_items = defaultdict(list)

    for item in vendor_recent_sales:
        vendor_daily_sales_items[item['timestamp']].append(item)

    # Sum of each order item made per day in the last x days
    daily_sales_totals = []

    for i in range(len(sales_date)):
        daily_sum = 0
        try:
            days_list = vendor_daily_sales_items[vendor_daily_sales_items.keys()[i]]
            if days_list is not None or len(days_list) > 0:
                items_totals = [x.get_total() for x in days_list]
                # Get total order price
                daily_sum = sum(items_totals)
        except:
            # less vendor products
            pass
        daily_sales_totals.append(daily_sum)

    # Combine the two list for serialization
    data = list(zip(sales_date, daily_sales_totals))

    data_to_list = []
    for item in data:
        item = list(item)
        data_to_list.append(item)

    # Combine the list generated to the original for serialization
    daily_sales += data_to_list

    return daily_sales


def formulate_vendors_order_status(vendor) -> list:
    chart_label = 'Status % Totals'

    # Vendors order items data
    vendor_recent_sales = OrderItem.objects.filter(vendor=vendor)

    vendor_daily_sales_items = defaultdict(list)

    for item in vendor_recent_sales:
        vendor_daily_sales_items[item['status']].append(item)

    # Set status to count values
    pending = len(vendor_daily_sales_items["P"])
    on_transit = len(vendor_daily_sales_items["T"])
    cancelled = len(vendor_daily_sales_items["C"])
    delivered = len(vendor_daily_sales_items["D"])

    order_stats = [
        ['Order', chart_label],
        ['On Transit', on_transit],
        ['Cancelled', cancelled],
        ['Pending', pending],
        ['Delivered', delivered],
    ]

    return order_stats


def count_my_customers() -> int:
    return 0


def calculate_order_stream() -> float:
    return 0


def dashboard_analytics(request):
    active_users = User.objects.filter(is_active=True).count()
    vendor = get_object_or_404(Vendor, user=request.user)

    # All order items to this vendor
    orders = len(OrderItem.objects.filter(vendor=vendor))

    # Count customers who bought something from this shop
    customers = count_my_customers()
    # order stream %
    order_stream = calculate_order_stream()
    # Get delivered orders
    # items_sold = formulate_vendors_order_status(vendor)[:-1]

    items_sold = len(OrderItem.objects.filter(vendor=vendor, status="D"))
    # Serialize order fulfilment statistics

    order_stats = dumps(formulate_vendors_order_status(vendor))
    # print(order_stats)

    # Serialize daily sales totals
    daily_sales = dumps(formulate_daily_sales())

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

    if request.method == "POST":
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
                  {'categories': categories, 'current_category': None})


# edit product
def edit_product(request, id):
    product = get_object_or_404(Product, id=id)
    categories = Category.objects.all()
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)

        # print(request.POST)
        # print(form.errors)

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
                   })


# delete product
def delete_product(request, id):
    user = request.user
    vendor = get_object_or_404(Vendor, user=user)
    product = get_object_or_404(Product, id=id)
    if product.vendor == vendor:
        product.delete()
        messages.success(request, "Product deleted successfully")
        return redirect('products')
    messages.error(request, "The delete operation failed")
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
        vendors = Vendor.objects.all()
        vendors = [vendor for vendor in vendors if vendor.brand is not None]
        serializer = VendorSerializer(vendors, many=True)
        return Response(serializer.data)

import datetime
from json import dumps
from collections import defaultdict

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import get_object_or_404, render, redirect
from django.template.loader import render_to_string
from django.utils import timezone
from cart.models import Cart, CartItem
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
from vendor.forms import ContactForm, ShopCreateForm,ShopForm
from vendor.models import Vendor
from vendor.serializers import VendorSerializer


def dashboard_register(request):
    form = UserCreationForm(request.POST)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            email_to = form.cleaned_data.get("email")
            scheme = request.build_absolute_uri().split(":")[0]
            path = f"{scheme}://{request.get_host()}/login"
            message = render_to_string("registration_email.html", {
                "email": email_to, "path": path})
            subject = "Registration confirmation"

            EmailThead([email_to], message, subject).start()

            messages.info(request, "Account created, check your email,login to start")
            try:
                vendor_user = get_object_or_404(User, email=form.cleaned_data.get("email"))
                if vendor_user:
                    user = authenticate(username=vendor_user.email, password=form.cleaned_data.get("password"))
                    if user:
                        login(request, user)
                        return redirect("create_shop")
            except:
                return redirect("login")

        else:
            print(form.errors)
    return render(request, "auth/register.html",
                  {"title": "Account creation"})


def dashboard_login(request):
    if request.POST:
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                try:
                    print("Searching vendor")
                    vendor = get_object_or_404(Vendor, user=user)
                    print("vendor found")
                    if vendor.brand is not None:
                        print("Vendor redirect to analytics")
                        return redirect('analytics')
                except:
                    print("Vendor nor found")
                    return redirect('create_shop')
            else:
                messages.error(request, "Incorrect email or password")
        else:
            messages.error(request, form.errors)
    return render(request, "auth/login.html", {"title": "Account lo"})


def create_shop(request):
    if request.POST and request.FILES:
        print(request.FILES)
        user = request.user

        form = ShopCreateForm(request.POST,request.FILES)
        print(form)
        print(form.is_valid())
        
        if form.is_valid():
            print("Form is valid check")
            vendor=form.save(commit=False)
            vendor.user=user
            vendor.save()
            print("Shop has been saved")
            messages.info(request, "Your shop has been saved successfully")
            print("now is redirecting check")
            return redirect("analytics")
        else:
            print(form.errors)
            messages.error(request, form.errors)
    print("Failed to get into post body")
    return render(request, "auth/shop.html")


def dashboard_analytics(request):
    # active_users = User.objects.filter(is_active=True).count()
    # vendor = get_object_or_404(Vendor, user=request.user)

    # # All order items to this vendor
    # orders = len(CartItem.objects.filter(vendor=vendor))

    # # Count customers who bought something from this shop
    # customers = count_my_customers()
    # # order stream %
    # order_stream = calculate_order_stream()
    # # Get delivered orders
    # # items_sold = formulate_vendors_order_status(vendor)[:-1]

    # items_sold = len(CartItem.objects.filter(vendor=vendor, status="D"))
    # # Serialize order fulfilment statistics

    # order_stats = dumps(formulate_vendors_order_status(vendor))
    # # print(order_stats)

    # # Serialize daily sales totals
    # daily_sales = dumps(formulate_daily_sales())

    # context = {"title": "Vendor dashboard analytics", "active_users": active_users, "order_stream": order_stream,
    #            "customers": customers, "items_sold": items_sold, "orders": orders, "order_stats": order_stats,
    #            "daily_sales": daily_sales}

    return render(request, "dashboard/analytics.html",)

def shop_update(request):
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

        messages.info(request, "Shop Updated successfully")
        return redirect("shop_update")
    print(form.errors)
    return render(request, "dashboard/shop_update.html",{"vendor":vendor})


def dashboard_orders(request,status):
    vendor = get_object_or_404(Vendor, user=request.user)
    items = CartItem.objects.all()

    if status== "P":
        items = CartItem.objects.filter(status="P")
    elif status == "T":
        items = CartItem.objects.filter(status="T")
    elif status == "F":
        items = CartItem.objects.filter(status="F")
    elif status == "C":
        items = CartItem.objects.filter(status="C")
    else:
        items = CartItem.objects.all()

    orders=[]

    for item in items:
        if item.product.vendor == vendor:
            # if item.order not in orders:
            orders.append(item)

    return render(request, "dashboard/orders.html",{"title": "orders", "orders": orders})


# def manage_orders(request, id):
#     vendor = get_object_or_404(Vendor, user=request.user)
#     order = get_object_or_404(Cart, id=id)
#     order_items = CartItem.objects.filter(order=order)

#     orders = []

#     for order_item in order_items:
#         if order_item.product.vendor == vendor:
#             orders.append(order_item)

#     return render(request, "vendor/manage-orders.html",
#                   {"title": "Manage orders", "order_items": order_items})


def dashboard_products(request):
    vendor = get_object_or_404(Vendor, user=request.user)
    products = Product.objects.filter(vendor=vendor)

    return render(request, "dashboard/products.html",
                  {"title": "My products", "products": products})


# product create
def create_product(request):
    categories = Category.objects.all()
    form = ProductForm(request.POST, request.FILES)
    
    if request.method == "POST" and form.is_valid():
        product = form.save(commit=False)
        product.vendor = get_object_or_404(Vendor, user=request.user)
        product.save()
        print("product saved")
        messages.success(request, f"{product.label} added successfully")
        return redirect('products')
    else:
        messages.error(request, f"{form.errors}")
    return render(request, "dashboard/products_create.html",
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

        messages.info(request, "Help message received")
        return redirect("analytics")
    return render(request, "dashboard/contact.html",
                  {"title": "Help contact"})



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
    vendor_recent_sales = CartItem.objects.filter(timestamp__lt=timezone.now() - datetime.timedelta(days=10))

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
    vendor_recent_sales = CartItem.objects.filter(vendor=vendor)

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

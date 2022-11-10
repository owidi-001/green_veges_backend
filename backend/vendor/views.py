
from json import dumps
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import get_object_or_404, render, redirect
from django.template.loader import render_to_string
from cart.models import CartItem
from product.forms import ProductForm
from product.models import Category
from product.models import Product
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from user.forms import UserCreationForm
# signup COMPLETE
from user.forms import UserLoginForm
from user.models import User
from user.views import EmailThead
from vendor.forms import ContactForm, ShopCreateForm,ShopForm
from vendor.models import Vendor
from vendor.serializers import VendorSerializer
from vendor.utils import customers_streamed, daily_sales_totals, order_status, orders_streamed, pending_orders, top_selling, total_earnings


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
    vendor = get_object_or_404(Vendor, user=request.user)
    # total incoming orders for this vendor
    total_orders=orders_streamed(request)
    
    # pending orders
    pending=pending_orders(request)
    
    # total unique customers for this vendor
    total_customers=customers_streamed(request)
    
    # Total earnings
    sales_total=total_earnings(request)


    # products by number of orders made
    top_selling_products=top_selling(request)

    # order stats count
    order_stats=dumps(order_status(request))
    
    # daily sales total
    daily_sales=dumps(daily_sales_totals(request))
    print(daily_sales)

    context={
        "total_orders":total_orders,
        "total_customers":total_customers,
        "sales_total":sales_total,
        "pending_orders":pending,
        "top_selling":top_selling_products,
        "order_stats": order_stats,
        "daily_totals":daily_sales,
        "vendor":vendor
    }

    return render(request, "dashboard/analytics.html",context=context)


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

    return render(request, "dashboard/orders.html",{"title": "orders", "orders": orders,"vendor":vendor})


def manage_order(request, id):

    vendor = get_object_or_404(Vendor, user=request.user)

    order = get_object_or_404(CartItem, id=id)

    status_color="#23AA49"
    riders=[]

    if order.status=="P":
        status_color="#f0b802"
        riders=[1,2,3,4,5]
    elif order.status == "T":
        status_color="##979899"
    elif order.status == "C":
        status_color="#FF324B"

    if order:
        return render(request, "dashboard/order_detail.html",{"title": "Manage order", "order": order,"status_color":status_color,"riders":riders,"vendor":vendor})



def dashboard_products(request):
    vendor = get_object_or_404(Vendor, user=request.user)
    products = Product.objects.filter(vendor=vendor)

    return render(request, "dashboard/products.html",
                  {"title": "My products", "products": products,"vendor":vendor})


# product create
def create_product(request):
    vendor = get_object_or_404(Vendor, user=request.user)
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
                  {'categories': categories, 'current_category': None,"vendor":vendor})


# edit product
def update_product(request, id):
    vendor = get_object_or_404(Vendor, user=request.user)
    product = get_object_or_404(Product, id=id)
    categories = Category.objects.all()
    
    
    if request.POST:
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
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
        else:
            messages.error(request, 'Product update failed')


    return render(request, "dashboard/products_edit.html",
                  {'product': product, 'categories': categories, 'current_category': product.category,"vendor":vendor
                   })


# delete product
def delete_product(request,id):
    product = get_object_or_404(Product, id=id)
    try:
        product.delete()
        messages.success(request, "Product deleted successfully")
        return redirect('products')
    except:
        messages.error(request, "Unable to delete this product")


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
                  {"title": "Help contact","vendor":vendor})




class VendorViews(APIView):
    """ Vendor dashboard functions: list, create, update, delete for products"""

    authentication_classes = [TokenAuthentication]
    permission_classes = [AllowAny]

    """ Gets a list of all products belonging to the vendor """

    def get(self, request):
        vendors = Vendor.objects.all()
        serializer = VendorSerializer(vendors, many=True)
        return Response(serializer.data,status=status.HTTP_200_ok)

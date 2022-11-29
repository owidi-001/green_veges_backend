
from collections import defaultdict
from datetime import datetime
import datetime
from django.utils import timezone
from django.shortcuts import get_object_or_404

from cart.models import CartItem
from vendor.models import Vendor


# helper function to get vendor orders
def vendor_orders(request):
    vendor = get_object_or_404(Vendor, user=request.user)
    
    try:
        items = CartItem.objects.all()
        vendor_items=[]
        for item in items:
            if item.get_vendor==vendor:
                vendor_items.append(item)
        return vendor_items
    except:
        return []



# orders streamed
def orders_streamed(request)->int:
    try:
        return len(vendor_orders(request))
    except:
        return 0

def pending_orders(request):
    vendor_items=vendor_orders(request)

    # filters only complete orders
    pending_items=[item for item in vendor_items if item.status=="Pending"]

    try:
        return len(pending_items)
    except:
        return 0


def customers_streamed(request)->int:
    try:
        vendor_items=vendor_orders(request)
        customers=[]
        for item in vendor_items:
            if item.get_customer not in customers:
                customers.append(item.get_customer)

        return len(customers)
    except:
        return 0

def top_selling(request):
    # returns the top 3 selling products by order quantity count
    vendor_items=vendor_orders(request)
    
    products={}

    for item in vendor_items:
        if item.get_product_id not in products:
            products[item.get_product_id]=item.quantity
        else:
            products[item.get_product_id]+=item.quantity

    if len(products) <= 2:
        return products
    else:
        from operator import itemgetter
        # top N items to be gotten
        N = 3
        res = dict(sorted(products.items(), key = itemgetter(1), reverse = True)[:N])

        return res


def total_earnings(request):
    vendor_items=vendor_orders(request)

    # filters only complete orders
    delivered_items=[item for item in vendor_items if item.status=="Completed"]

    try:
        total=sum([item.get_total for item in delivered_items])
        return total
    except:
        return 0



def order_status(request):
    vendor_items=vendor_orders(request)

    # order stats count
    delivered=len([item for item in vendor_items if item.status=="Completed"])
    on_transit=len([item for item in vendor_items if item.status=="On Transit"])
    pending=len([item for item in vendor_items if item.status=="Pending"])
    cancelled=len([item for item in vendor_items if item.status=="Cancelled"])
    
    if delivered == on_transit == pending == cancelled == 0:
        delivered=1
        on_transit=1
        pending=1
        cancelled=1

    order_stats = [
        ['Delivered', delivered],
        ['On Transit', on_transit],
        ['Cancelled', cancelled],
        ['Pending', pending],
    ]

    return order_stats


# daily sales totals
def daily_sales_totals(request):
    
    # last ten dates from today
    sale_dates = [(timezone.now() - datetime.timedelta(days=i)).date() for i in range(10)]
    vendor_items=vendor_orders(request)

    date_totals={}

    for sale_date in sale_dates:
        totals=0
        for item in vendor_items:
            if sale_date == item.get_order_date.date():
                totals+=item.get_total

        date_totals[str(sale_date)]=float(totals)

    data=[
        ['Date', 'Sales total']
    ]
    x=[[k,v] for k,v in date_totals.items()]
    x.reverse()
    return data + x


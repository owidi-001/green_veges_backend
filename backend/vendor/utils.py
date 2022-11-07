
from collections import defaultdict
from datetime import datetime, timezone
from django.utils import timezone

from cart.models import CartItem


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


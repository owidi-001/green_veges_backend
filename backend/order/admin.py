from django.contrib import admin
from .models import OrderItem, Order, Feedback, Address


class OrderAdmin(admin.ModelAdmin):
    list_display = ["customer", "date", "total", "status"]
    list_filter = ["date", "status", "customer"]


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ["order", "product", "quantity", "status", "get_total"]
    list_filter = ["order", "product", "status"]


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(Address)
admin.site.register(Feedback)

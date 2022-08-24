from django.contrib import admin
from .models import OrderItem, Order, Feedback


class OrderAdmin(admin.ModelAdmin):
    list_display = ["customer", "date", "total", "status"]
    list_filter = ["date", "status", "customer"]


admin.site.register(Order,OrderAdmin)
admin.site.register(OrderItem)
admin.site.register(Feedback)

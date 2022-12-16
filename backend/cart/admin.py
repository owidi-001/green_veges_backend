from django.contrib import admin

# Register your models here.
from .models import Cart, Location, CartItem


class CartAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "status",
        "date_ordered",
        "location",
    ]
    list_filter = ["user",
                   "status",
                   "date_ordered",
                   "location", ]


class CartItemAdmin(admin.ModelAdmin):
    list_display = [
        "cart",
        "status",
        "product",
        "quantity",
        "date",
        "time",
    ]
    list_filter = ["cart",
                   "product",
                   ]


class LocationAdmin(admin.ModelAdmin):
    list_display = [
        "name", "block_name", "floor_number", "room_number"
    ]


admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)
admin.site.register(Location, LocationAdmin)

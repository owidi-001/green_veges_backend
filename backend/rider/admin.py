from django.contrib import admin

# Register your models here.

from .models import Rider, VendorRider, OrderRider


class RiderAdmin(admin.ModelAdmin):
    list_filter = ['user','brand' ,'license','national_id']
    list_display = ['user', "license",'national_id']
    search_fields = ["license"]


class VendorRiderAdmin(admin.ModelAdmin):
    list_filter = ['vendor', 'rider']
    list_display = ['vendor', "rider"]
    search_fields = ["rider"]


class OrderRiderAdmin(admin.ModelAdmin):
    list_filter = ['item', 'rider']
    list_display = ['item', "rider"]
    search_fields = ["rider"]


admin.site.register(Rider, RiderAdmin)
admin.site.register(VendorRider, VendorRiderAdmin)
admin.site.register(OrderRider, OrderRiderAdmin)

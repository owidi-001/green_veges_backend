from django.contrib import admin
from .models import Vendor, VendorRider


class VendorAdmin(admin.ModelAdmin):
    list_filter = ['user', 'brand']
    list_display = ['user', "brand"]
    search_fields = ["brand"]


class VendorRiderAdmin(admin.ModelAdmin):
    list_filter = ['vendor', 'rider']
    list_display = ['vendor', "rider"]
    search_fields = ["rider"]

admin.site.register(Vendor, VendorAdmin)
admin.site.register(VendorRider, VendorRiderAdmin)

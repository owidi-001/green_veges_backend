from django.contrib import admin
from .models import Vendor


class VendorAdmin(admin.ModelAdmin):
    list_filter = ['user', 'brand']
    list_display = ['user', "brand"]
    search_fields = ["brand"]


admin.site.register(Vendor, VendorAdmin)

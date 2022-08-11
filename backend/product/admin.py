from django.contrib import admin
from .models import Category, Product, Property


class CategoryAdmin(admin.ModelAdmin):
    list_filter = ["name", ]
    list_display = ["name", ]


class ProductAdmin(admin.ModelAdmin):
    list_filter = ["label", "category"]
    list_display = ["label", "unit_price", "category"]


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Property)

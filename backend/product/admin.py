from django.contrib import admin
from .models import Category, Product


class CategoryAdmin(admin.ModelAdmin):
    list_filter = ["name", ]
    list_display = ["name", ]


class ProductAdmin(admin.ModelAdmin):
    list_filter = ["category", "vendor"]
    list_display = ["label", "unit_price", "category", "vendor"]


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)

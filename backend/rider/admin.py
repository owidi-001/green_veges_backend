from django.contrib import admin

# Register your models here.

from .models import Rider


class RiderAdmin(admin.ModelAdmin):
    list_filter = ['user','license']
    list_display = ['user', "license"]
    search_fields = ["license"]


admin.site.register(Rider, RiderAdmin)

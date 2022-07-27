from django.contrib import admin

from .models import Client

# Register your models here.
class ClientAdmin(admin.ModelAdmin):
    list_display=["user","address"]
    list_filter=["user","address"]

admin.site.register(Client,ClientAdmin)    
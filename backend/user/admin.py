from django.contrib import admin
from .models import User

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_filter = ['username', 'email', 'is_staff','is_active']
    list_display = ['username', 'email', 'first_name',
                    'last_name', 'is_staff']
    search_fields=["email","username"]                


admin.site.register(User,UserAdmin)

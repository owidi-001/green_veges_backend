from django.contrib import admin
from .models import User


# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_filter = ['email', 'is_staff', 'is_active']
    list_display = ['first_name', "last_name", 'email', 'phone_number',
                    'is_staff']
    search_fields = ["email", "phone_number"]


admin.site.register(User, UserAdmin)

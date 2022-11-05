from django.contrib import admin
from .models import Payment


# Register your models here.
class PaymentAdmin(admin.ModelAdmin):
    list_display = ["user", "mpesaReceiptNumber", "phone", "amount", "transactionDate"]
    list_filter = ["user", "mpesaReceiptNumber", "phone", "transactionDate"]


admin.site.register(Payment, PaymentAdmin)

from django.db import models

from cart.models import Cart

from user.models import User


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    mpesaReceiptNumber = models.CharField(max_length=20)
    balance = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    transactionDate = models.DateTimeField()
    phone = models.CharField(max_length=13)
    

    class Meta:
        verbose_name = 'Mpesa Payment'
        verbose_name_plural = 'Mpesa Payments'

    def __str__(self):
        return self.mpesaReceiptNumber

from django.db import models
from cart.models import CartItem
from user.models import User

from vendor.models import Vendor


# Create your models here.
class Rider(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    license = models.CharField(max_length=9)

    def __str__(self) -> str:
        return self.user.email


class VendorRider(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    rider = models.ForeignKey(Rider, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.vendor}:{self.rider}"


class OrderRider(models.Model):
    item = models.ForeignKey(CartItem, on_delete=models.CASCADE)
    rider = models.ForeignKey(Rider, on_delete=models.CASCADE)

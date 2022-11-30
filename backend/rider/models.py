from django.db import models
from cart.models import CartItem, Location
from user.models import User

from vendor.models import Vendor


# Create your models here.
class Rider(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    brand=models.CharField(max_length=50,null=True,blank=True)
    dob=models.CharField(max_length=10,blank=True,null=True)
    national_id = models.CharField(max_length=8,blank=True,null=True)
    license = models.CharField(max_length=9)

    def __str__(self) -> str:
        return self.brand


class VendorRider(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    rider = models.ForeignKey(Rider, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.vendor}:{self.rider}"


class OrderRider(models.Model):
    item = models.ForeignKey(CartItem, on_delete=models.CASCADE)
    rider = models.ForeignKey(Rider, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE,null=True,blank=True)


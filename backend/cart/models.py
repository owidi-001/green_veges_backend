from django.db import models

# Create your models here.
from django.utils import timezone
from product.models import Product

from user.models import User

from .utils import randomString


class Location(models.Model):
    lng = models.FloatField(
        null=True,
        blank=True,
    )
    lat = models.FloatField(
        null=True,
        blank=True,
    )
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    street = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "location"

    def __str__(self):
        return f"{self.street},{self.city},Kenya"


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    STATUS = (("Pending", "Pending"), ("Processing", "Processing"), ("Fulfilled", "Fulfilled"))
    status = models.CharField(max_length=10, choices=STATUS, default="Pending")
    date_ordered = models.DateTimeField(auto_now_add=timezone.now())
    location = models.ForeignKey(
        Location,
        on_delete=models.PROTECT,
        related_name="address", null=True, blank=True
    )

    @property
    def date(self):
        return self.date_ordered.strftime("%d %B, %Y")

    class Meta:
        verbose_name_plural = "Cart"

    def __str__(self):
        return f"Cart: {self.user}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    class Meta:
        unique_together = ("cart", "product")

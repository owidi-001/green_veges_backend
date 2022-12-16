from django.db import models

# Create your models here.
from django.utils import timezone
from product.models import Product

from user.models import User


class Location(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    block_name = models.CharField(max_length=100, blank=True, null=True)
    floor_number = models.CharField(max_length=5, blank=True, null=True)
    room_number = models.CharField(max_length=5, blank=True, null=True)

    class Meta:
        verbose_name_plural = "location"

    def __str__(self):
        return f"{self.name}"


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    STATUS = (
        ("Pending", "Pending"), ("On Transit", "On Transit"), ("Completed", "Completed"), ("Cancelled", "Cancelled"))
    status = models.CharField(max_length=20, choices=STATUS, default="Pending")
    date_ordered = models.DateTimeField(auto_now_add=timezone.now())
    location = models.ForeignKey(
        Location,
        on_delete=models.PROTECT,
        related_name="address", null=True, blank=True
    )
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        ordering=["-date_ordered"]

    @property
    def date(self):
        return self.date_ordered.strftime("%d %B, %Y")

    @property
    def get_address(self) -> str:
        return f"""Place name: {self.location.name}
                Block: {self.location.block_name}
                Floor: {self.location.floor_number}
                Room:{self.location.room_number}"""
    @property
    def get_address_name(self) -> str:
        return self.location.name

    @property
    def get_address_block(self) -> str:
        return  self.location.block_name

    @property
    def get_address_floor(self) -> str:
        return self.location.floor_number
               
    @property
    def get_address_room(self) -> str:
        return self.location.room_number

    class Meta:
        verbose_name_plural = "Cart"

    def __str__(self):
        return f"Cart: {self.user}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    status=models.CharField(max_length=20,choices=(("Completed","Completed"),("Cancelled","Cancelled"),("On Transit","On Transit"),("Pending","Pending")),default="Pending")
    date=models.DateTimeField(auto_now_add=timezone.now())
    time = models.TimeField(auto_now_add=True)

    class Meta:
        unique_together = ("cart", "product")

    @property
    def get_total(self) -> float:
        return self.product.unit_price * self.quantity

    @property
    def get_vendor(self):
        return self.product.vendor

    @property
    def get_customer(self):
        return self.cart.user

    @property
    def get_product_id(self) -> int:
        return self.product.id

    @property
    def get_order_date(self):
        return self.cart.date_ordered

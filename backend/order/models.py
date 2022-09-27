from django.db import models

# Create your models here.
from client.models import Client
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.utils import timezone

from user.views import EmailThead

from user.models import User

from product.models import Product


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, default="Un named")
    lat = models.FloatField()
    long = models.FloatField()
    floor_number = models.IntegerField(blank=True, null=True)
    door_number = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return f"{self.name}"


class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=1,
        choices=(
            ("P", "Pending"),
            ("O", "In Progress"),
            ("C", "Cancelled"),
            ("F", "Fulfilled"),
        ),
        default="P",
        db_index=True
    )
    date = models.DateTimeField(verbose_name='order date', auto_now_add=True)
    total = models.IntegerField()
    delivery_address = models.ForeignKey(Address, null=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'order'
        verbose_name_plural = 'orders'
        ordering = ('-date',)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    status = models.CharField(
        max_length=1,
        choices=(
            ("R", "Received"),
            ("T", "On Transit"),
            ("D", "Delivered"),
            ("C", "Cancelled"),
        ),
        default="R",
        db_index=True
    )

    def get_total(self):
        return self.product.unit_price * self.quantity

    def __str__(self):
        return f"Order:{self.order}, Name: {self.product.label}, Quantity:{self.quantity}, Total:{self.get_total()}"


class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    order = models.OneToOneField(
        Order, on_delete=models.CASCADE, default=None)
    message = models.TextField()
    created_on = models.DateTimeField(auto_created=True, default=timezone.now)
    rating = models.IntegerField(default=1)

    class Meta:
        verbose_name_plural = "Feedback"

    def __str__(self):
        return f"{self.user}: {self.message}"


# send notification when the order is delivered
@receiver(post_save, sender=Order)
def send_customer_notification(sender=None, instance=None, created=False, **kwargs):
    try:
        if instance.status == "F":
            clients = OrderItem.objects.filter(
                order=instance.order, status="D"
            )
            message = "Delivery has arrived."

            # email notification
            EmailThead(
                [item.order.customer.email for item in clients] +
                [settings.EMAIL_HOST_USER], message
            )

    except:
        pass

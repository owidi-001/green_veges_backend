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


class Order(models.Model):
    customer = models.OneToOneField(Client, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=1,
        choices=(
            ("R", "Received"),
            ("P", "Processing"),
            ("C", "Cancelled"),
            ("D", "Delivered"),
        ),
        default="R",
        db_index=True
    )
    date = models.DateTimeField(verbose_name='creation date')
    total = models.IntegerField()

    class Meta:
        verbose_name = 'cart'
        verbose_name_plural = 'carts'
        ordering = ('-date',)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)


class ClientOrder(models.Model):
    client = models.OneToOneField(Client, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("order", "client")

    def __str__(self) -> str:
        return f"{self.client.user.email} :{self.order}"


class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    order = models.OneToOneField(
        Order, on_delete=models.CASCADE, default=None)
    message = models.TextField()
    created_on = models.DateTimeField(auto_created=True, default=timezone.now)

    class Meta:
        verbose_name_plural = "Feedback"

    def __str__(self):
        return f"{self.user}: {self.message}"


# send notification when the order is delivered
@receiver(post_save, sender=ClientOrder)
def send_customer_notification(sender=None, instance=None, created=False, **kwargs):
    try:
        if instance.status == "F":
            clients = ClientOrder.objects.filter(
                order=instance.order, status="D"
            )
            message = "You delivery has arrived"

            # email notification
            EmailThead(
                [item.customer.email for item in clients] +
                [settings.EMAIL_HOST_USER], message
            )

    except:
        pass

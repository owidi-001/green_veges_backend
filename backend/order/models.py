from django.db import models

# Create your models here.
from client.models import Client
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.utils import timezone

from user.views import EmailThead

from user.models import User


class Order(models.Model):
    client = models.OneToOneField(Client, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=1,
        choices=(
            ("R", "Received"),
            ("P", "Pending"),
            ("C", "Cancelled"),
            ("D", "Delivered"),
        ),
        default="P",
        db_index=True
    )
    creation_date = models.DateTimeField(verbose_name='creation date')
    checked_out = models.BooleanField(default=False, verbose_name='checked out')
    price = models.IntegerField()
    rating = models.FloatField(
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = 'cart'
        verbose_name_plural = 'carts'
        ordering = ('-creation_date',)


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

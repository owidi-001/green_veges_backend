from django.db import models
from user.models import User



# Address
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


# Create your models here.
class Client(models.Model):
    user=models.OneToOneField(User,models.CASCADE)
    address=models.ForeignKey(Location,on_delete=models.PROTECT,
        related_name="location",)
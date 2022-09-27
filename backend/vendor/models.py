from django.db import models

from user.models import User


# Create your models here.
class Vendor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    brand = models.CharField(max_length=50, null=True)
    logo = models.ImageField(upload_to="vendors/%Y/%m/%d/", null=True)
    tagline = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.brand


class HelpMessage(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.PROTECT)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    upload = models.FileField(upload_to='uploads/%Y/%m/%d/', null=True, blank=True)

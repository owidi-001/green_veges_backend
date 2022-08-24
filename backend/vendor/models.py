from django.db import models

from user.models import User


# Create your models here.
class Vendor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.email


class HelpMessage(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.PROTECT)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    upload = models.FileField(upload_to='uploads/%Y/%m/%d/', null=True, blank=True)

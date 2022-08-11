from django.db import models
from user.models import User


# Create your models here.
class Client(models.Model):
    user = models.OneToOneField(User, models.CASCADE)

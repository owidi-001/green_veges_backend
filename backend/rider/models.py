from django.db import models
from user.models import User

# Create your models here.
class Rider(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    license=models.CharField(max_length=9)

    def __str__(self) -> str:
        return self.user.email        
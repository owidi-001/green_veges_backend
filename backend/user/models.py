from django.contrib.auth.models import AbstractUser
from django.db import models
# Generates auth token
from django.db.models.signals import post_save
from rest_framework.authtoken.models import Token

# local modules
from .managers import UserManager


def upload(instance, filename):
    return f"media/{instance.user.id}/{filename}"


class User(AbstractUser):
    # first_name = models.CharField(max_length=30, blank=False, unique=True)
    # last_name = models.CharField(max_length=30, blank=False, unique=True)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(
        max_length=13, null=False, blank=False, unique=True)
    is_vendor = models.BooleanField(default=False, blank=True)
    username = None
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "phone_number"]
    objects = UserManager()

    def __str__(self) -> str:
        return f"{self.email}"


"""
 Generate authentication  token after a user has been created and send him/her an email
"""


def create_user(sender, instance, created, **kwargs):
    if created:
        auth_token = Token.objects.create(user=instance)

        auth_token.save()


post_save.connect(create_user, sender=User)


class PasswordResetToken(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    short_token = models.IntegerField(null=True)
    reset_token = models.CharField(max_length=100)

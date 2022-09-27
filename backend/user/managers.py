from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email, phone_number, password=None):

        if not email:
            raise ValueError("User must have an email")
        if not phone_number:
            raise ValueError("User must have a phone number")

        if not password:
            raise ValueError("User must have a secure password")

        user = self.model(
            email=self.normalize_email(email)
        )
        user.phone_number = phone_number
        user.set_password(password)  # changes password to hash
        user.is_admin = False
        user.is_staff = False
        user.save(using=self._db)
        return user

    def create_superuser(self, email, phone_number, password=None):

        user = self.model(
            email=self.normalize_email(email)
        )
        user.phone_number = phone_number
        user.set_password(password)  # changes password to hash
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

    def create_staff(self, email, phone_number, password=None):

        user = self.model(
            email=self.normalize_email(email)
        )
        user.phone_number = phone_number
        user.set_password(password)  # changes password to hash
        user.is_admin = False
        user.is_staff = True
        user.is_superuser = False
        user.save(using=self._db)
        return user

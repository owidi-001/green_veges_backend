from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, first_name, last_name, email, phone_number, password=None):
        if not first_name:
            raise ValueError("Please fill in your first name")
        if not last_name:
            raise ValueError("Please fill in your first name")
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
        user.first_name = first_name
        user.last_name = last_name
        user.set_password(password)  # changes password to hash
        user.is_admin = False
        user.is_staff = False
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, email, phone_number, password=None):

        user = self.model(
            email=self.normalize_email(email)
        )
        user.phone_number = phone_number
        user.first_name = first_name
        user.last_name = last_name
        user.set_password(password)  # changes password to hash
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

    def create_staff(self, first_name, last_name, email, phone_number, password=None):

        user = self.model(
            email=self.normalize_email(email)
        )
        user.phone_number = phone_number
        user.first_name = first_name
        user.last_name = last_name
        user.set_password(password)  # changes password to hash
        user.is_admin = False
        user.is_staff = True
        user.is_superuser = False
        user.save(using=self._db)
        return user

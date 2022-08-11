from django import forms

from django.core.exceptions import ValidationError

from user.validators import phone_number_validator
from user.validators import email_validator


class ClientProfileUpdateForm(forms.Form):
    first_name = forms.CharField(
        max_length=150, help_text="First name is required")
    last_name = forms.CharField(
        max_length=150, help_text="Last name is required")
    phone_number = forms.CharField(required=False, max_length=13)
    email = forms.EmailField(required=False)

    def clean_phone_number(self):
        phone_no = self.cleaned_data.get("phone_number")
        if phone_no and not phone_number_validator(phone_no):
            raise ValidationError(
                "please provide valid phone number eg +254712345678")
        return phone_no

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if not email:
            raise ValidationError("Please provide your email address")
        if not email_validator(email):
            raise ValidationError(
                "please provide a valid Email address")
        return email

    def clean_first_name(self):
        first_name = self.cleaned_data.get("first_name")
        if not first_name:
            raise ValidationError("First name is required")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get("last_name")
        if not last_name:
            raise ValidationError("Last name is required")
        return last_name
from django import forms
from .models import User
from django.core.exceptions import ValidationError
from .validators import phone_number_validator, email_validator


class UserCreationForm(forms.ModelForm):
    email = forms.EmailField(help_text="Email is required")
    phone_number = forms.CharField(
        max_length=13, help_text="Phone number is required")
    first_name = forms.CharField(
        max_length=150, help_text="First name is required")
    is_vendor = forms.BooleanField(required=False, help_text="I want to be a vendor")

    class Meta:
        model = User
        fields = ["phone_number", "email", "first_name", "last_name", "password", "is_vendor"]

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if not email:
            raise ValidationError("Please provide your email address")
        if not email_validator(email):
            raise ValidationError(
                "please provide a valid Email address")
        return email

    def clean_phone_number(self):
        phone_no = self.cleaned_data.get("phone_number")
        if not phone_no:
            raise ValidationError("please provide your phone number")
        if not phone_number_validator(phone_no):
            raise ValidationError(
                "please provide valid phone number eg 0712345678")
        return phone_no

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

    def clean_is_vendor(self):
        is_vendor = self.cleaned_data.get("is_vendor")
        if not is_vendor:
            return False
        return True

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class UserLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(max_length=150, widget=forms.PasswordInput)


class ResetPasswordForm(forms.Form):
    password1 = forms.PasswordInput()
    password2 = forms.PasswordInput()

    def clean_password1(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if not (password1 == password2):
            raise ValidationError("Passwords don't match")
        return password1


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(help_text="Email is required")
    phone_number = forms.CharField(
        max_length=13, help_text="Phone number is required")
    first_name = forms.CharField(
        max_length=150, help_text="First name is required")
    is_vendor = forms.BooleanField(required=False, help_text="I want to be a vendor")

    class Meta:
        model = User
        fields = ["phone_number", "email", "first_name", "last_name", "password", "is_vendor"]

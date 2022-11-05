from django import forms

from vendor.models import HelpMessage

from vendor.models import Vendor


class ShopForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields = ['brand', "tagline", "logo"]


class ContactForm(forms.ModelForm):
    class Meta:
        model = HelpMessage
        fields = ['subject', "message", "upload"]

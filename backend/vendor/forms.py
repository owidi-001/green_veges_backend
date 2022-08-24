from django import forms

from vendor.models import HelpMessage


class ContactForm(forms.ModelForm):
    class Meta:
        model = HelpMessage
        fields = ['subject', "message", "upload"]

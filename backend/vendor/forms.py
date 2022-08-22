from django import forms


class ContactForm(forms.Form):
    subject = forms.CharField(max_length=200)
    message = forms.Textarea()
    email = forms.EmailField()


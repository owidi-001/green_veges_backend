from django import forms

class ProductForm(forms.Form):
    name=forms.CharField(max_length=200)
    price=forms.FloatField()
    image=forms.ImageField()
    description=forms.TextField()
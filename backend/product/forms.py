from django import forms

from product.models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["label", "unit_price", "description", "quantity"]

    # label = forms.CharField(max_length=200)
    # unit_price = forms.DecimalField(max_digits=5, decimal_places=2)
    image = forms.FileField()
    # description = forms.CharField(max_length=500)
    # quantity = forms.IntegerField()


class ProductUpdateForm(forms.Form):
    label = forms.CharField(max_length=200)
    unit_price = forms.DecimalField(max_digits=5, decimal_places=2)
    description = forms.CharField(max_length=500)
    quantity = forms.IntegerField()

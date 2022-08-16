from django import forms


class ProductForm(forms.Form):
    label = forms.CharField(max_length=200)
    unit_price = forms.DecimalField(max_digits=5, decimal_places=2)
    image = forms.ImageField()
    description = forms.CharField(max_length=500)
    quantity = forms.IntegerField()


class ProductUpdateForm(forms.Form):
    label = forms.CharField(max_length=200)
    unit_price = forms.DecimalField(max_digits=5, decimal_places=2)
    description = forms.CharField(max_length=500)
    quantity = forms.IntegerField()

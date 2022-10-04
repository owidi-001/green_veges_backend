from django import forms

from order.models import Order, OrderItem, Address, Feedback


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ["name", "lat", "long", "floor_number", "door_number"]


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ["order", "message", "rating"]


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["total", "delivery_address"]


class OrderUpdateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["id", "status"]


class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ["order", "product", "quantity"]


class OrderItemUpdateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["status"]


class OrderDeleteForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["id"]

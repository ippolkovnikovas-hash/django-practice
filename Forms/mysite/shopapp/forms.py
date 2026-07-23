from django import forms

from shopapp.models import Product, Order


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name','price', 'description', 'discount')


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ("delivery_address", "promocode", "products")

        #widgets = {
        #    "products": forms.CheckboxSelectMultiple(),
        #    "delivery_address": forms.Textarea(attrs={"rows": 3}),
        #}
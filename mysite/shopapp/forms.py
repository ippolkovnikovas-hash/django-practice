from django import forms

from shopapp.models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name','price', 'description', 'discount')
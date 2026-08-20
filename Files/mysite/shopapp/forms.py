from django import forms
from django.contrib.auth.models import Group

from shopapp.models import Product, Order


class MultipleImageInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleImageField(forms.ImageField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleImageInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        clean_one_file = super().clean

        if isinstance(data, (list, tuple)):
            return [
                clean_one_file(file, initial)
                for file in data
            ]

        return [clean_one_file(data, initial)]


class ProductForm(forms.ModelForm):
    images = MultipleImageField(
        required=False,
        label="Дополнительные изображения",
    )

    class Meta:
        model = Product
        fields = (
            "name",
            "price",
            "description",
            "discount",
            "preview",
        )

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ("delivery_address", "promocode", "products")

class GroupsForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ["name"]
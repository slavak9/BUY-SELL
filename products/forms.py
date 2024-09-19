from django import forms
from shopping_cart.models import UserCart
from products.models import ProductName

class AddProductInCart(forms.ModelForm):
    class Meta:
        model = UserCart
        fields = ['product_id', 'quantity', 'user_id']

class ProductNameForm(forms.ModelForm):
    class Meta:
        model = ProductName
        fields = ['title', 'slug', 'is_published', 'price', 'quantity', 'products_item']
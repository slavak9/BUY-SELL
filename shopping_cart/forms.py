from django import forms
from shopping_cart.models import ItemsToPurchase

class AddItemsToPurchase(forms.ModelForm):
    class Meta:
        model = ItemsToPurchase
        fields = ['user_id', 'json_data']


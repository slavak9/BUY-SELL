from django import forms
from products.models.transport import *


class CarsForm(forms.ModelForm):
    class Meta:  
        model = Cars
        fields = ['brand', 'year', 'price', 'brand_choices_to_select']



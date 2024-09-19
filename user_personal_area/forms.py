from django import forms
from user_personal_area.models import UserShippingAddress



class AddUserShippingAddress(forms.ModelForm):
    class Meta:
        model = UserShippingAddress
        fields = ['user_id', 'country', 'region', 'locality_or_city', 'street','is_chosen',
                  'home_apartment', 'postal_zip_code', 'phone_number', 'other_information']


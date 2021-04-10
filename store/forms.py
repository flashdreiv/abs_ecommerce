from django import forms
from .models import DeliveryInfo

class CheckOutForm(forms.ModelForm):
    class Meta:
        model = DeliveryInfo
        fields = ['mobile_number','address','province','city','zipcode',]



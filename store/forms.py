from django import forms
from .models import DeliveryInfo
from ph_locations.models import Province,City
from store.models import Customer
from allauth.account.forms import SignupForm
from . models import SmsCode

class CheckOutForm(forms.ModelForm):
    class Meta:
        model = DeliveryInfo
        fields = ['mobile_number','address','province','city','zipcode',]

class CustomerSignupForm(SignupForm):
    def __init__(self, *args, **kwargs):
        super(CustomerSignupForm, self).__init__(*args, **kwargs)
        self.fields['first_name'] = forms.CharField(required=True)
        self.fields['last_name'] = forms.CharField(required=True)
        self.fields['mobile_number'] = forms.CharField(required=True,max_length=11,min_length=11)
        self.fields['address'] = forms.CharField(required=True)
        self.fields['province'] = forms.ModelChoiceField(queryset=Province.objects.all(),required=True)
        self.fields['city'] = forms.ModelChoiceField(queryset=City.objects.all(),required=True)

    def save(self,request):
        
        user = super(CustomerSignupForm, self).save(request)
        mobile_number = self.cleaned_data.pop('mobile_number')
        address = self.cleaned_data.pop('address')
        province = self.cleaned_data.pop('province')
        city = self.cleaned_data.pop('city')
        user.username = mobile_number
        user.save()
        Customer.objects.create(user=user,mobile_number=mobile_number,address=address,province=province,city=city)
    
        return user

class CodeForm(forms.ModelForm):
    class Meta:
        model = SmsCode
        fields = ['code']
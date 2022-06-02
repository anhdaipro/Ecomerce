from order.models import Coupon,OrderItem
from django.db import models
from django.forms.models import ModelForm
from django.forms import forms, widgets 
from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
class CouponForm(forms.Form):
    code = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Promo code',
        'aria-label': 'Recipient\'s username',
        'aria-describedby': 'basic-addon2'
    }))

METHOD_CHOICE=(
('N','Nhanh'),
("HT","Hỏa tốc"),
('TK','Tiết kiệm')
)
class ShippingForm(forms.Form):
    method=forms.ChoiceField(choices=METHOD_CHOICE)

class AddCartForm(forms.Form):
    quantity=forms.IntegerField()
    check=forms.BooleanField(required=False)
class CheckForm(forms.Form):
    check=forms.BooleanField(required=False)
    
PAYMENT_CHOICES = (
    ('S', 'Stripe'),
    ('P', 'PayPal'),
    ('After','Payment on delivery')
)

class CheckoutForm(forms.Form):
    shipping_address = forms.CharField(required=False)
    name=forms.CharField(required=False)
    phone_number=forms.CharField(required=False)
    city = forms.CharField(required=False)
    shipping_zip = forms.CharField(required=False)
    billing_address = forms.CharField(required=False)
    city2 = forms.CharField(required=False)
    same_billing_address = forms.BooleanField(required=False)
    set_default_shipping = forms.BooleanField(required=False)
    use_default_shipping = forms.BooleanField(required=False)
    set_default_billing = forms.BooleanField(required=False)
    use_default_billing = forms.BooleanField(required=False)
    payment_option = forms.ChoiceField(
        widget=forms.RadioSelect, choices=PAYMENT_CHOICES)

class PaymentForm(forms.Form):
    stripeToken = forms.CharField(required=False)
    save = forms.BooleanField(required=False)
    use_default = forms.BooleanField(required=False)

class RefundForm(forms.Form):
    ref_code = forms.CharField()
    message = forms.CharField(widget=forms.Textarea(attrs={
        'rows': 4
    }))
    email = forms.EmailField()

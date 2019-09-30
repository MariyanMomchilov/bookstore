from django import forms
from django.contrib.auth.models import User
from django_countries.fields import CountryField

PAYMENT_CHOICES = (('S', 'Stripe'),
                ('P', 'PayPal'))

class SignUp(forms.Form):
    username = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(label = 'Re-password',widget=forms.PasswordInput())
    first_name = forms.CharField(label='First name', max_length=100, required=False)
    last_name = forms.CharField(label='Last name', max_length=100, required=False)
    email = forms.EmailField()

class Checkout(forms.Form):
    #first_name = forms.CharField(label='First name', max_length=100)
    #last_name = forms.CharField(label='Last name', max_length=100)
    shipping_address = forms.CharField(label='Shipping address', max_length=200)
    country = CountryField(blank_label=('Select country')).formfield()
    zip = forms.CharField(label='Zip code', max_length=30)
    payment_option = forms.ChoiceField(widget=forms.RadioSelect(), choices = PAYMENT_CHOICES)
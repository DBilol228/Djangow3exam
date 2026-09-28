from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *

class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['phone_number','password1','password2']

class LoginForm(forms.Form):
    phone_number = forms.CharField()
    password = forms.CharField()

class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['first_name','last_name','address','passport_id']

class CardForm(forms.ModelForm):
    class Meta:
        model = Card
        fields = ['card_number','cvv','type','pin']

class TransferForm(forms.Form):
    phone_number = forms.CharField(required=False)
    card_number = forms.CharField(required=False)
    source = forms.CharField()
    source_card_number = forms.CharField(required=False)
    destination = forms.CharField()
    amount = forms.IntegerField()

class CheckPhoneForm(forms.Form):
    phone_number = forms.CharField()

class CheckCardForm(forms.Form):
    card_number = forms.CharField()
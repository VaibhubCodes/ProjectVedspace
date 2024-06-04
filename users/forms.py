# users/forms.py

from django import forms

class SignUpForm(forms.Form):
    mobile_number = forms.CharField(max_length=15)
    referral_id = forms.CharField(max_length=20, required=False)

class SignInForm(forms.Form):
    mobile_number = forms.CharField(max_length=15)

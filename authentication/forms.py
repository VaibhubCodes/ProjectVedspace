# authentication/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from users.models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'phone_number', 'password1', 'password2']

class OTPVerificationForm(forms.Form):
    otp = forms.CharField(max_length=6, required=True, label='Enter OTP')

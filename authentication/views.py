# authentication/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, login, authenticate
from django.http import JsonResponse
from twilio.rest import Client
from django.conf import settings
from .forms import CustomUserCreationForm, OTPVerificationForm

User = get_user_model()

def send_otp(phone_number):
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    verification = client.verify.services(settings.TWILIO_VERIFY_SERVICE_SID).verifications.create(to=phone_number, channel='sms')
    return verification.sid

def verify_otp(phone_number, otp):
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    verification_check = client.verify.services(settings.TWILIO_VERIFY_SERVICE_SID).verification_checks.create(to=phone_number, code=otp)
    return verification_check.status == 'approved'

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            send_otp(user.phone_number)
            return redirect('verify_otp', user_id=user.id)
    else:
        form = CustomUserCreationForm()
    return render(request, 'authentication/register.html', {'form': form})

def verify_otp_view(request, user_id):
    if request.method == 'POST':
        form = OTPVerificationForm(request.POST)
        if form.is_valid():
            otp = form.cleaned_data['otp']
            user = User.objects.get(id=user_id)
            if verify_otp(user.phone_number, otp):
                user.is_active = True
                user.save()
                login(request, user)
                return redirect('dashboard')
            else:
                return JsonResponse({'error': 'Invalid OTP'})
    else:
        form = OTPVerificationForm()
    return render(request, 'authentication/verify_otp.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            send_otp(user.phone_number)
            return redirect('verify_otp', user_id=user.id)
        else:
            return JsonResponse({'error': 'Invalid credentials'})
    return render(request, 'authentication/login.html')

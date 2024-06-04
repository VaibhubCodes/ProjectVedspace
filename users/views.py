# users/views.py

from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import logout
from .forms import SignUpForm, SignInForm
from .models import CustomUser

def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            request.session['mobile_number'] = form.cleaned_data['mobile_number']
            return redirect(reverse('social:begin', kwargs={'backend': 'google-oauth2'}))
    else:
        form = SignUpForm()
    return render(request, 'sign_up.html', {'form': form})

def sign_in(request):
    if request.method == 'POST':
        form = SignInForm(request.POST)
        if form.is_valid():
            mobile_number = form.cleaned_data['mobile_number']
            user = CustomUser.objects.filter(phone_number=mobile_number).first()
            if user:
                request.session['mobile_number'] = mobile_number
                return redirect(reverse('social:begin', kwargs={'backend': 'google-oauth2'}))
            else:
                form.add_error('mobile_number', 'No user with this mobile number found.')
    else:
        form = SignInForm()
    return render(request, 'sign_in.html', {'form': form})

def auth_complete(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        return redirect('sign_in')

def home(request):
    return render(request, 'home.html')

def logout_view(request):
    logout(request)
    return redirect('home')

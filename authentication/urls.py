from django.urls import path
from .views import register, verify_otp_view, login_view

urlpatterns = [
    path('register/', register, name='register'),
    path('verify-otp/<int:user_id>/', verify_otp_view, name='verify_otp'),
    path('login/', login_view, name='login'),
]

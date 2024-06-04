"""
URL configuration for VEDSPACE project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from users import views as user_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users', include('users.urls')),
    path('quiz/', include('quiz.urls')),
    path('', user_views.home, name='home'),
    path('sign_up/', user_views.sign_up, name='sign_up'),
    path('sign_in/', user_views.sign_in, name='sign_in'),
    path('logout/', user_views.logout_view, name='logout'),  # Add this line
    path('auth/complete/', user_views.auth_complete, name='auth_complete'),
    path('auth/', include('social_django.urls', namespace='social')),

]


from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('photo', 'bio', 'skills', 'education', 'college', 'age', 'gender', 'phone_number', 'instagram_profile', 'linkedin_profile', 'github_profile')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('photo', 'bio', 'skills', 'education', 'college', 'age', 'gender', 'phone_number', 'instagram_profile', 'linkedin_profile', 'github_profile')}),
    )
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff', 'college', 'phone_number', 'instagram_profile', 'linkedin_profile', 'github_profile']
    search_fields = ['username', 'first_name', 'last_name', 'email', 'skills', 'college', 'instagram_profile', 'linkedin_profile', 'github_profile']
    list_filter = UserAdmin.list_filter + ('college', 'skills',)

admin.site.register(CustomUser, CustomUserAdmin)

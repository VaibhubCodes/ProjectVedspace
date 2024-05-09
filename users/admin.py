from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django import forms
from django.core.exceptions import ValidationError
from .models import CustomUser, CompanyUser, CollegeUser

# Custom Forms for Creating and Changing Users

class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = CustomUser
        fields = ('email', 'password', 'is_active', 'is_admin')

    def clean_password(self):
        return self.initial["password"]

class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password Confirmation', widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ('email',)

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

# UserAdmin classes for each user type

class CustomUserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    list_display = ('email', 'is_admin', 'is_active')
    list_filter = ('is_admin', 'is_active')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('photo', 'bio', 'skills', 'education', 'college', 'age', 'gender', 'phone_number', 'instagram_profile', 'linkedin_profile', 'github_profile')}),
        ('Permissions', {'fields': ('is_admin', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_active', 'is_admin'),
        }),
        ('Personal Info', {
            'classes': ('wide',),
            'fields': ('photo', 'bio', 'skills', 'education', 'college', 'age', 'gender', 'phone_number', 'instagram_profile', 'linkedin_profile', 'github_profile'),
        }),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()

# Repeat similar setups for CompanyUser and CollegeUser if they have unique fields or requirements

class CompanyUserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    model = CompanyUser
    list_display = ('email', 'company_name', 'is_active')
    list_filter = ('is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Company Information', {'fields': ('company_name', 'website', 'description', 'employees', 'category', 'contact_number')}),
        ('Permissions', {'fields': ('is_active',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'company_name', 'website', 'description', 'employees', 'category', 'contact_number', 'is_active'),
        }),
    )
    search_fields = ('email', 'company_name')
    ordering = ('email',)
    filter_horizontal = ()

class CollegeUserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    model = CollegeUser
    list_display = ('email', 'college_name', 'is_active')
    list_filter = ('is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('College Information', {'fields': ('college_name', 'courses', 'tnp_cell_contact', 'category', 'number_of_students', 'social_profile')}),
        ('Permissions', {'fields': ('is_active',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'college_name', 'courses', 'tnp_cell_contact', 'category', 'number_of_students', 'social_profile', 'is_active'),
        }),
    )
    search_fields = ('email', 'college_name')
    ordering = ('email',)
    filter_horizontal = ()

# Register models with their respective admins
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(CompanyUser, CompanyUserAdmin)
admin.site.register(CollegeUser, CollegeUserAdmin)

from django.contrib.auth.models import AbstractUser
from django.db import models

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

# Manager for CustomUser
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        user = self.create_user(email, password=password, **extra_fields)
        user.is_admin = True
        user.save(using=self._db)
        return user

class CustomUser(AbstractBaseUser):
    DEGREE_CHOICES = [
        ('BTECH', 'B.Tech'),
        ('BCA', 'BCA'),
        ('MCA', 'MCA'),
        ('MBA', 'MBA'),
        ('BSC', 'B.Sc.'),
        ('BDES', 'B.Des'),
    ]
    email = models.EmailField(max_length=255, unique=True, null=True, blank=True)
    photo = models.ImageField(upload_to='user_photos/', null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    skills = models.CharField(max_length=255, null=True, blank=True)
    education = models.CharField(max_length=50, choices=DEGREE_CHOICES, null=True, blank=True)
    college = models.CharField(max_length=255, null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    gender = models.CharField(max_length=10, null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    instagram_profile = models.URLField(null=True, blank=True)
    linkedin_profile = models.URLField(null=True, blank=True)
    github_profile = models.URLField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        return True

    @property
    def is_staff(self):
        return self.is_admin

# Separate CompanyUser and CollegeUser models with similar attributes as CustomUser but managed separately
class CompanyUserManager(BaseUserManager):
    # Implementation similar to CustomUserManager
    pass

class CompanyUser(AbstractBaseUser):
    company_name = models.CharField(max_length=255)
    website = models.URLField(max_length=255)
    description = models.TextField()
    employees = models.IntegerField()
    category = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=15)
    email = models.EmailField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)  # Make sure this is defined
    is_admin = models.BooleanField(default=False)  # Administrative access to Django admin

    USERNAME_FIELD = 'email'
    objects = CompanyUserManager()

class CollegeUserManager(BaseUserManager):
    # Implementation similar to CustomUserManager
    pass

class CollegeUser(AbstractBaseUser):
    college_name = models.CharField(max_length=255)
    courses = models.TextField()
    tnp_cell_contact = models.CharField(max_length=255)
    category = models.CharField(max_length=100)
    number_of_students = models.IntegerField()
    social_profile = models.URLField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)  # Make sure this is defined
    is_admin = models.BooleanField(default=False)  # Administrative access to Django admin

    USERNAME_FIELD = 'email'
    objects = CollegeUserManager()
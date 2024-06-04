# users/models.py
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, username, email=None, phone_number=None, password=None, **extra_fields):
        if not username:
            raise ValueError('The Username must be set')
        email = self.normalize_email(email) if email else None
        user = self.model(username=username, email=email, phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email=None, phone_number=None, password=None, **extra_fields):
        user = self.create_user(username, email, phone_number, password, **extra_fields)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user

class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, unique=True, primary_key=True)
    phone_number = models.CharField(max_length=15, unique=True, null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(max_length=255, unique=True, null=True, blank=True)
    photo = models.ImageField(upload_to='user_photos/', null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    skills = models.CharField(max_length=255, null=True, blank=True)
    education = models.CharField(max_length=50, null=True, blank=True)
    college = models.CharField(max_length=255, null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    gender = models.CharField(max_length=10, null=True, blank=True)
    instagram_profile = models.URLField(null=True, blank=True)
    linkedin_profile = models.URLField(null=True, blank=True)
    github_profile = models.URLField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    groups = models.ManyToManyField('auth.Group', related_name='customuser_set', blank=True)
    user_permissions = models.ManyToManyField('auth.Permission', related_name='customuser_permissions_set', blank=True)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'phone_number']

    objects = CustomUserManager()

    def __str__(self):
        return self.username

class CompanyUserManager(BaseUserManager):
    def create_user(self, username, email=None, password=None, **extra_fields):
        if not username:
            raise ValueError('The Username must be set')
        email = self.normalize_email(email) if email else None
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        user = self.create_user(username, email, password, **extra_fields)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user

class CompanyUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, unique=True, primary_key=True,default='username')
    company_name = models.CharField(max_length=255)
    website = models.URLField(max_length=255)
    description = models.TextField()
    employees = models.IntegerField()
    category = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=15)
    phone_number = models.CharField(max_length=15, unique=True, null=True, blank=True)
    email = models.EmailField(max_length=255, unique=True, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    groups = models.ManyToManyField('auth.Group', related_name='companyuser_set', blank=True)
    user_permissions = models.ManyToManyField('auth.Permission', related_name='companyuser_permissions_set', blank=True)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    objects = CompanyUserManager()

    def __str__(self):
        return self.username

class CollegeUserManager(BaseUserManager):
    def create_user(self, username, email=None, password=None, **extra_fields):
        if not username:
            raise ValueError('The Username must be set')
        email = self.normalize_email(email) if email else None
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        user = self.create_user(username, email, password, **extra_fields)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user

class CollegeUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, unique=True, primary_key=True, default='username')
    college_name = models.CharField(max_length=255)
    courses = models.TextField()
    tnp_cell_contact = models.CharField(max_length=255)
    category = models.CharField(max_length=100)
    number_of_students = models.IntegerField()
    social_profile = models.URLField(max_length=255)
    phone_number = models.CharField(max_length=15, unique=True, null=True, blank=True)
    email = models.EmailField(max_length=255, unique=True, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    groups = models.ManyToManyField('auth.Group', related_name='collegeuser_set', blank=True)
    user_permissions = models.ManyToManyField('auth.Permission', related_name='collegeuser_permissions_set', blank=True)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    objects = CollegeUserManager()

    def __str__(self):
        return self.username

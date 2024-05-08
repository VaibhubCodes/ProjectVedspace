from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):

    DEGREE_CHOICES = [
        ('BTECH', 'B.Tech'),
        ('BCA', 'BCA'),
        ('BBA', 'BBA'),
        ('MCA', 'MCA'),
        ('MBA', 'MBA'),
        ('BSC', 'B.Sc.'),
        ('BDES', 'B.Des'),
    ]
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

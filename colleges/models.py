# colleges/models.py

from django.db import models

class College(models.Model):
    name = models.CharField(max_length=255)
    university = models.CharField(max_length=255)

    def __str__(self):
        return self.name

from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=50)
    date_of_birth = models.DateField(max_length=50, null=True)
    sex = models.CharField(max_length=10, null=True)
    role = models.CharField(max_length=10, default='Student')

    def __str__(self):
        return self.name

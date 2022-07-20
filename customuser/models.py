from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=500)
    date_of_birth = models.DateField(null=True)
    phone_number = models.BigIntegerField()
    sex = models.CharField(max_length=10, null=True)
    role = models.CharField(max_length=20, default='Student')
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'sex', 'role', 'phone_number', 'username']

    def __str__(self):
        return self.email


class UserPayment(models.Model):
    payee_book = models.ForeignKey('library_books.Book',
                                   on_delete=models.CASCADE)
    payer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    description = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=50, default='Pending')
    amount = models.CharField(max_length=50, default='O UGX')

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.description[0:20]

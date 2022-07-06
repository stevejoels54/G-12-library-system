from django.db import models


class Books(models.Model):
    title = models.CharField(max_length=200)
    book_code = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    subject_area = models.CharField(max_length=200)
    publication_date = models.DateField()
    status = models.CharField(max_length=50, default="Available")
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    borrower_id = models.BigIntegerField()
    due_date = models.DateTimeField(null=True, blank=True)


def __str__(self):
    return self.title


class Payments(models.Model):
    book_id = models.BigIntegerField()
    description = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=50, default='Pending')
    amount = models.CharField(max_length=50, default='O UGX')
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.description[0:20]

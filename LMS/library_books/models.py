from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    subject_area = models.CharField(max_length=200)
    publication_date = models.DateField()
    status = models.CharField(max_length=50, default="Available")
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    borrower_id = models.ForeignKey(
        'customuser.CustomUser', on_delete=models.SET_NULL, null=True, blank=True)
    due_date = models.DateTimeField(null=True, blank=True)


def __str__(self):
    return self.title


class Request(models.Model):
    status = models.CharField(max_length=20, default="Pending")
    requester_id = models.ForeignKey(
        'customuser.CustomUser', on_delete=models.CASCADE)
    book_id = models.ForeignKey(Book, on_delete=models.CASCADE)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.status

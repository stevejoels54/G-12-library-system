from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Book


def addBook(request):
    return render(request, 'library_books/books.html', {})


@login_required(login_url='/login/')
def dashboard(request):
    books = Book.objects.all()
    context = {'books': books}
    return render(request, "library_books/dashboard.html", context)

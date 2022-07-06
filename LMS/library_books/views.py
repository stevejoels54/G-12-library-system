from django.shortcuts import render
from django.contrib.auth.decorators import login_required


def addBook(request):
    return render(request, 'library_books/books.html', {})


@login_required(login_url='/login/')
def dashboard(request):
    return render(request, "library_books/dashboard.html", {})

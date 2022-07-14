from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Book, Request
from customuser.models import CustomUser


def addBook(request):
    return render(request, 'library_books/books.html', {})


@login_required(login_url='/login/')
def dashboard(request, pk):
    context = {}
    books = Book.objects.filter(status="Available")
    user = CustomUser.objects.get(id=pk)
    total_books = Book.objects.all()
    users = CustomUser.objects.filter(role='Student')
    pending_requests = Request.objects.filter(status="Pending")
    librarian = CustomUser.objects.get(role__icontains="Admin")
    if request.user.role == 'Student':
        borrowed_book = Book.objects.get(borrower_id=user.id)
    else:
        borrowed_book = ''

    if user.role.lower() == 'student':
        context = {
            'books': books,
            'user': user,
            'users': users.count(),
            'total_books': total_books.count(),
            'pending_requests': pending_requests.count(),
            'librarian': librarian,
            'borrowed_book': borrowed_book
        }
        if request.method == "POST":
            value = request.POST.get("value")
            books = Book.objects.filter(
                title__icontains=value) | Book.objects.filter(
                    author__icontains=value) | Book.objects.filter(
                        subject_area__icontains=value)
            context['books'] = books
            return render(request, 'library_books/dashboard.html', context)

    elif user.role.lower() == 'admin':
        books = Book.objects.filter(status="Available")
        context = {
            'books': books,
            'user': user,
            'users': users.count(),
            'total_books': total_books.count(),
            'pending_requests': pending_requests.count(),
            'librarian': librarian,
            'borrowed_book': borrowed_book
        }
        if request.method == "POST":
            value = request.POST.get("value")
            books = Book.objects.filter(
                title__icontains=value) | Book.objects.filter(
                    author__icontains=value) | Book.objects.filter(
                        subject_area__icontains=value)
            context['books'] = books
            return render(request, 'library_books/dashboard.html', context)
    return render(request, "library_books/dashboard.html", context)


@login_required(login_url='/login/')
def borrowBook(request, book, pk):
    context = {}
    book = Book.objects.get(id=book)
    if request.method == "POST":
        """ book.borrower = user
            book.status = "Borrowed"
            book.save() """
        print("Book id is: ", book.title)
        return redirect("/dashboard/" + pk)
    return render(request, 'library_books/dashboard.html', context)

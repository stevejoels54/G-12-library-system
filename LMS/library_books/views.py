from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Book, Request
from customuser.models import CustomUser
from datetime import datetime


@login_required(login_url='/login/')
def addBook(request):
    userID = request.user.id
    if request.method == "GET":
        title = request.GET.get("title")
        author = request.GET.get("author")
        subject_area = request.GET.get("subject_area")
        status = "Available"
        created = datetime.now()
        if title != None and author != None and subject_area != None:
            book = Book(title=title,
                        author=author,
                        subject_area=subject_area,
                        status=status,
                        publication_date=created,
                        created=created)
            book.save()
            return redirect("/dashboard/" + str(userID))
        return redirect('/dashboard/' + str(userID))
    return redirect('/dashboard/' + str(userID))


@login_required(login_url='/login/')
def dashboard(request, pk):
    context = {}
    books = Book.objects.filter(status="Available")
    total_books = Book.objects.all()
    users = CustomUser.objects.filter(role='Student')
    pending_requests = Request.objects.filter(status="Pending")
    librarian = CustomUser.objects.get(role__icontains="Admin")
    try:
        user = CustomUser.objects.get(id=pk)
    except:
        user = None
    try:
        borrowed_book = Book.objects.get(borrower_id=user.id)
    except:
        borrowed_book = ''
    context = {
        'books': books,
        'user': user,
        'users': users.count(),
        'total_books': total_books.count(),
        'pending_requests': pending_requests.count(),
        'librarian': librarian,
        'borrowed_book': borrowed_book
    }

    if user != None:
        if user.role.lower() == 'student':
            books = Book.objects.filter(status="Available")
            context['books'] = books
            return render(request, 'library_books/dashboard.html', context)

        elif user.role.lower() == 'admin':
            books = Book.objects.all()
            context['books'] = books
            return render(request, 'library_books/dashboard.html', context)
    else:
        print("Invalid user")
        return redirect('/pageNotFound/')

    return render(request, "library_books/dashboard.html", context)


@login_required(login_url='/login/')
def borrowBook(request, book, pk):
    context = {}
    try:
        book = Book.objects.get(id=book)
    except:
        book = None
        pass
    try:
        user = CustomUser.objects.get(id=pk)
    except:
        user = None
        pass
    if request.method == "GET":
        if book != None and user != None:
            if user.role.lower() != 'admin' and user.role.lower() == 'student':
                if book.status == "Available":
                    try:
                        borrowed_book = Book.objects.get(borrower_id=user.id)
                    except:
                        borrowed_book = None
                    if borrowed_book is None:
                        book.status = "Pending"
                        book.save()
                        book_request = Request(requester_id=user,
                                               book_id=book,
                                               status="Pending")
                        book_request.save()
                        return redirect('/dashboard/' + str(pk))
                    else:
                        print("You have already borrowed a book")
                        return redirect('/dashboard/' + str(pk))
                else:
                    print("Book is not available")
                    return redirect('/dashboard/' + str(pk))
            elif user.role.lower() == 'admin':
                print("Admin can not borrowed a book")
                return redirect('/dashboard/' + str(pk))
        else:
            print("Invalid user or book")
            return redirect('/pageNotFound/')
    return redirect('/dashboard/' + str(pk))


@login_required(login_url='/login/')
def searchBook(request):
    context = {}
    userID = request.user.id
    user = CustomUser.objects.get(id=userID)
    books = Book.objects.filter(status="Available")
    total_books = Book.objects.all()
    users = CustomUser.objects.filter(role='Student')
    pending_requests = Request.objects.filter(status="Pending")
    librarian = CustomUser.objects.get(role__icontains="Admin")
    try:
        borrowed_book = Book.objects.get(borrower_id=userID)
    except:
        borrowed_book = ''
    query = request.GET.get('value')
    context = {
        'books': books,
        'user': user,
        'users': users.count(),
        'total_books': total_books.count(),
        'pending_requests': pending_requests.count(),
        'librarian': librarian,
        'borrowed_book': borrowed_book
    }
    if request.method == "GET":
        value = request.GET.get("value")
        print("Value is: ", value)
        if user.role.lower() == 'admin' and value != None:
            books = Book.objects.filter(
                title__icontains=value) | Book.objects.filter(
                    author__icontains=value) | Book.objects.filter(
                        subject_area__icontains=value)
            context['books'] = books
            return render(request, 'library_books/dashboard.html', context)

        elif user.role.lower() == 'student' and value != None:
            books = Book.objects.filter(
                title__icontains=value) | Book.objects.filter(
                    author__icontains=value) | Book.objects.filter(
                        subject_area__icontains=value)
            books = books.filter(status="Available")
            context['books'] = books
            return render(request, 'library_books/dashboard.html', context)

        elif user.role.lower() == 'admin' and value == None:
            books = Book.objects.all()
            context['books'] = books
            return render(request, 'library_books/dashboard.html', context)
        elif user.role.lower() == 'student' and value == None:
            books = Book.objects.all()
            context['books'] = books
            books = books.filter(status="Available")
            return render(request, 'library_books/dashboard.html', context)

    return render(request, 'library_books/dashboard.html', context)

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Book, Request
from customuser.models import CustomUser, UserPayment
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
    borrowed_books = 0
    available_books = 0
    users = CustomUser.objects.filter(role='Student')
    pending_requests = Request.objects.filter(status="Pending")
    fines = UserPayment.objects.filter(status='Pending')
    librarian = CustomUser.objects.get(role__icontains="Admin")

    try:
        available_books = Book.objects.filter(status='Available').count()
    except:
        available_books = 0
    try:
        borrowed_books = Book.objects.filter(status='Borrowed').count()
    except:
        borrowed_books = 0

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
        'pending_requests': pending_requests.count(),
        'fines': fines.count(),
        'librarian': librarian,
        'borrowed_book': borrowed_book,
        'available_books': available_books,
        'borrowed_books': borrowed_books,
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
                    try:
                        request = Request.objects.get(requester_id=user)
                    except:
                        request = None
                    if borrowed_book is None and request is None:
                        book.status = "Pending"
                        book.save()
                        book_request = Request(requester_id=user,
                                               book_id=book,
                                               status="Pending")
                        book_request.save()
                        return redirect('/dashboard/' + str(pk))
                    else:
                        return redirect('/dashboard/' + str(pk))
                else:
                    return redirect('/dashboard/' + str(pk))
            elif user.role.lower() == 'admin':
                return redirect('/dashboard/' + str(pk))
        else:
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
    fines = UserPayment.objects.filter(status='Pending')
    try:
        borrowed_book = Book.objects.get(borrower_id=userID)
    except:
        borrowed_book = ''
    try:
        available_books = Book.objects.filter(status='Available').count()
    except:
        available_books = 0
    try:
        borrowed_books = Book.objects.filter(status='Borrowed').count()
    except:
        borrowed_books = 0
    query = request.GET.get('value')
    context = {
        'books': books,
        'user': user,
        'users': users.count(),
        'total_books': total_books.count(),
        'pending_requests': pending_requests.count(),
        'librarian': librarian,
        'borrowed_book': borrowed_book,
        'available_books': available_books,
        'borrowed_books': borrowed_books,
        'fines': fines.count(),
    }
    if request.method == "GET":
        value = request.GET.get("value")
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


@login_required(login_url='/login/')
def bookAction(request):
    user = request.user.id
    if request.method == "GET":
        delete = request.GET.get("Delete")
        update = request.GET.get("Update")
        if delete != None:
            book = Book.objects.get(id=delete)
            book.delete()
            return redirect('/dashboard/' + str(user))

        elif update != None:
            return redirect('/dashboard/' + str(user))
    return redirect('/dashboard/' + str(user))


@login_required(login_url='/login/')
def returnBook(request, pk):
    user = request.user.id
    if request.method == "GET":
        try:
            book = Book.objects.get(id=pk)
        except:
            book = None
        try:
            request = Request.objects.get(requester_id=user)
        except:
            request = None
        if book != None and request != None:
            book.status = "Available"
            book.borrower_id = None
            book.save()
            request.delete()
            return redirect('/dashboard/' + str(user))
    return redirect('/dashboard/' + str(user))

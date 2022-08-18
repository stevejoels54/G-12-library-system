from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import CustomUser, UserPayment
from library_books.models import Book, Request
from datetime import datetime, timedelta


@login_required(login_url='login')
def userProfile(request, pk):
    user = CustomUser.objects.get(id=pk)
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
        borrowed_book = Book.objects.get(status='Borrowed',
                                         borrower_id=user.id)
    except:
        borrowed_book = ''

    context = {
        'users': users.count(),
        'pending_requests': pending_requests.count(),
        'fines': fines.count(),
        'librarian': librarian,
        'borrowed_book': borrowed_book,
        'available_books': available_books,
        'borrowed_books': borrowed_books,
    }
    return render(request, 'customuser/profile_template.html', context)


@login_required(login_url='login')
def userPayments(request, pk):
    details = {}
    payment = ''
    borrowed_book = ''
    borrowed_books = 0
    available_books = 0
    user = CustomUser.objects.get(id=pk)
    total_books = Book.objects.all()
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
        borrowed_book = Book.objects.get(status='Borrowed',
                                         borrower_id=user.id)
    except:
        borrowed_book = ''

    if request.user.role == 'Admin':
        details = {}  # Main dictionary containing all others
        payments = ''
        book = ''
        index = 0  # Counter

        try:  # Get all users
            students = CustomUser.objects.all()
        except:
            return HttpResponse('No students yet')

        for student in students:
            if student.role == 'Student':
                # Initialize individual student dictionaries
                details[index] = {}
                try:
                    # Access keys inside inner dictionaries
                    details[index]['name'] = student.name
                    details[index]['phone_number'] = student.phone_number
                except:
                    details[index]['name'] = ''
                    details[index]['phone_number'] = ''

                try:
                    book = Book.objects.get(borrower_id=student.id)
                    details[index]['title'] = book.title
                    details[index]['due_date'] = book.due_date
                except:
                    book = ''
                    details[index]['title'] = ''
                    details[index]['due_date'] = ''

                try:
                    payment = UserPayment.objects.get(payer=student.id)
                    details[index]['amount'] = payment.amount
                except:
                    # Terminate entry if no payment exists
                    payment = ''

                if details[index][
                        'title'] == '':  # Delete indexes without books
                    details.pop(index)

                index += 1

        context = {'details': details}

    else:
        student = CustomUser.objects.get(id=pk)
        try:
            book = Book.objects.get(borrower_id=student.id)
            payment = UserPayment.objects.get(payer=student.id)
        except:
            # Sort payment error
            payment = ''
            book = ''

    context = {
        'details': details,
        'users': users.count(),
        'pending_requests': pending_requests.count(),
        'fines': fines.count(),
        'librarian': librarian,
        'borrowed_book': borrowed_book,
        'available_books': available_books,
        'borrowed_books': borrowed_books,
        'payment': payment,
        'book': book
    }

    return render(request, 'customuser/payments_template.html', context)


@login_required(login_url='login')
def userNotifications(request, pk):
    template_details = {}
    details = {}
    borrowed_book = ''
    borrowed_books = 0
    available_books = 0
    borrow_request = ''
    index = 0
    requests = None

    user = CustomUser.objects.get(id=pk)
    users = CustomUser.objects.filter(role='Student')
    user = CustomUser.objects.get(id=pk)
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
        borrowed_book = Book.objects.get(status='Borrowed',
                                         borrower_id=user.id)
    except:
        borrowed_book = ''

    try:
        students = CustomUser.objects.filter(role='Student')
    except:
        return HttpResponse('No students yet')
    try:
        requests = Request.objects.filter(requester_id=user)
    except:
        requests = None
    requests_pending = Request.objects.all().filter(status="Pending")

    context = {
        'details': requests_pending,
        'users': users.count(),
        'pending_requests': pending_requests.count(),
        'fines': fines.count(),
        'librarian': librarian,
        'borrowed_book': borrowed_book,
        'available_books': available_books,
        'borrowed_books': borrowed_books,
        'requests': requests,
    }
    return render(request, 'customuser/notifications_template.html', context)


@login_required(login_url='login')
def requestAction(request, pk):
    if request.method == "GET":
        Accept = request.GET.get("Accept")
        Decline = request.GET.get("Decline")
        if Accept != None:
            accepted_request = Request.objects.get(book_id=Accept)
            borrowed_book = Book.objects.get(id=Accept)
            accepted_request.status = "Accepted"
            borrowed_book.status = 'Borrowed'
            borrowed_book.borrower_id = CustomUser.objects.get(id=pk)
            borrowed_book.due_date = datetime.now() + timedelta(hours=168)
            borrowed_book.save()
            accepted_request.save()
            return redirect('/user-notifications/' + str(request.user.id))

        elif Decline != None:
            accepted_request = Request.objects.get(book_id=Decline)
            borrowed_book = Book.objects.get(id=Decline)
            accepted_request.status = "Declined"
            borrowed_book.status = 'Available'
            borrowed_book.borrower_id = CustomUser.objects.get(id=pk)
            borrowed_book.due_date = datetime.now() + timedelta(hours=168)
            borrowed_book.save()
            accepted_request.save()
            return redirect('/user-notifications/' + str(request.user.id))

    return redirect('/user-notifications/' + str(request.user.id))


def home(request):
    return render(request, "home.html", {})

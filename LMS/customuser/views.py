from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import CustomUser, UserPayment
from library_books.models import Book


@login_required(login_url='login')
def userProfile(request, pk):
    user = CustomUser.objects.get(id=pk)

    context = {'user': user}
    return render(request, 'customuser/profile_template.html', context)


@login_required(login_url='login')
def userPayments(request, pk):
    user = CustomUser.objects.get(id=pk)
    details = {}
    payments = {}

    borrowed_books = Book.objects.filter(status='Borrowed')

    for book in borrowed_books:
        student = CustomUser.objects.get(id=book.borrower_id)
        payment = UserPayment.objects.get(status='Pending')
        payments[student.name] = payment.amount
        details[student.name] = book

    role = user.role
    borrowed_book = Book.objects.get(id=user.id)

    context = {'role': role, 'user': user, 'payments': payments,
               'borrowed_book': borrowed_book, 'details': details}

    return render(request, 'customuser/payments_template.html', context)


@login_required(login_url='login')
def userNotifications(request, pk):
    user = CustomUser.objects.get(id=pk)

    context = {'user': user}

    return render(request, 'customuser/notifications_template.html', context)

def home(request):
    return render(request, "home.html", {})

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import CustomUser, UserPayment
from library_books.models import Book, Request


@login_required(login_url='login')
def userProfile(request, pk):
    user = CustomUser.objects.get(id=pk)

    context = {'user': user}
    return render(request, 'customuser/profile_template.html', context)


@login_required(login_url='login')
def userPayments(request, pk):
    details = {}  # Main dictionary containing all others
    index = 0  # Counter

    try:  # Get all users
        students = CustomUser.objects.all()
    except:
        return HttpResponse('No students yet')

    for student in students:
        if student.role == 'Student':
            details[index] = {}  # Initialize individual student dictionaries
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
                details[index]['title'] = ''
                details[index]['due_date'] = ''

            try:
                payment = UserPayment.objects.get(payer=student.id)
                details[index]['amount'] = payment.amount
            except:
                details[index] = ''  # Make whole index dictionary empty

            index += 1

    context = {'details': details}

    return render(request, 'customuser/payments_template.html', context)


@login_required(login_url='login')
def userNotifications(request, pk):
    details = {}
    index = 0

    try:
        students = CustomUser.objects.all()
    except:
        return HttpResponse('No students yet')

    for student in students:
        if student.role == 'Student':
            details[index] = {}
            try:
                details[index]['name'] = student.name
                details[index]['phone_number'] = student.phone_number
            except:
                details[index]['name'] = ''
                details[index]['phone_number'] = ''

            try:
                # Get all book requests by a student
                book_request = Request.objects.get(requester_id=student.id)
                details[index]['time_requested'] = book_request.created
                # Get information about book requested
                book = Book.objects.get(id=book_request.book_id.id)
                details[index]['title'] = book.title
            except:
                details[index] = ''

            index += 1

    context = {'details': details}
    return render(request, 'customuser/notifications_template.html', context)

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from customuser.models import CustomUser
from library_books.models import Book, Request
from .forms import signupForm
from datetime import datetime
from django.contrib.auth.hashers import make_password, check_password

global user


def getUser(request, pk):
    user = CustomUser.objects.get(id=pk)


@login_required(login_url='/login/')
def leftMenu(request, pk):
    return render(request, "left_menu_template.html", {'user': user})


@login_required(login_url='/login/')
def base(request, pk):
    return render(request, "base.html", {'user': user})


@login_required(login_url='/login/')
def homeView(request):
    return render(request, "home_page.html", {})


@login_required(login_url='/login/')
def logoutUser(request):
    logout(request)
    return redirect('login')


def loginView(request):
    context = {}
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        context["email"] = email
        context["password"] = password
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect("/dashboard/" + str(user.id))
        else:
            messages.error(request, "Invalid email or password")
            return render(request, "login_page.html", context)

    return render(request, "login_page.html")


def signup(request):
    context = {}
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        role = request.POST.get('role')
        sex = request.POST.get('sex')
        date_of_birth = request.POST.get('date_of_birth')
        username = request.POST.get('username')
        context["name"] = name
        context["email"] = email
        context["phone_number"] = phone_number
        context["confirm_password"] = confirm_password
        context["role"] = role
        context["sex"] = sex
        context["date_of_birth"] = date_of_birth
        context["date_joined"] = datetime.now()
        context["username"] = username
        context["is_active"] = True
        context["password"] = password
        new_user = signupForm(context)

        if new_user.is_valid():
            if password == confirm_password:
                context["password"] = make_password(password)
                new_user = signupForm(context)
                if role == "Admin":
                    try:
                        user = CustomUser.objects.get(role=role)
                    except:
                        user = None

                    if user is None:
                        new_user.save()
                        messages.success(request, "User created successfully")
                        return redirect("/login/")
                    else:
                        context["password"] = password
                        messages.error(
                            request,
                            "Administrator already exists, signup as student")
                        return render(request, "signup.html", context)
                else:
                    new_user.save()
                    messages.success(request, "User created successfully")
                    return redirect("/login/")
            else:
                messages.error(request, "Passwords do not match")
                return render(request, "signup.html", context)
        else:
            context["password"] = password
            messages.error(request, new_user.errors)
            return render(request, "signup.html", context)
    return render(request, 'signup.html')


def home(request):
    return render(request, "home.html", {})

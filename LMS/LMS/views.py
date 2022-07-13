from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from customuser.models import CustomUser
from library_books.models import Book, Request

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
        username = request.POST.get("username")
        password = request.POST.get("password")
        context["username"] = username
        context["password"] = password
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("/dashboard/" + str(user.id))
        else:
            context["error"] = "Invalid username or password"
            messages.error(request, "Invalid username or password")
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
        context["name"] = name
        context["email"] = email
        context["phone_number"] = phone_number
        context["password"] = password
        context["confirm_password"] = confirm_password
        context["role"] = role
        context["sex"] = sex
        context["date_of_birth"] = date_of_birth
        print(role)
        #new_user = CustomUser.objects.create_user(name, email, password, role, sex, date_of_birth)

        if (password != confirm_password):
            messages.error(request, "Password should match confirm password")

        #return redirect('/signup/')

    return render(request, 'signup.html')


def home(request):
    return render(request, "home.html", {})

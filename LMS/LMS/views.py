from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from customuser.models import CustomUser


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
            return redirect("home")
        else:
            context["error"] = "Invalid username or password"
            messages.error(request, "Invalid username or password")
            return render(request, "login_page.html", context)

    return render(request, "login_page.html")


def signup(request):
    if request.method == "POST":
        user_name = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        new_user = User.objects.create_user(user_name, email, password)
        new_user = CustomUser.objects.create_user(user_name, email, password)
        new_user.first_name = first_name
        new_user.last_name = last_name

        return redirect('/login/')

    return render(request, 'signup.html')

def home(request):
        return render(request, "home.html", {})

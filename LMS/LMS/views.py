from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


@login_required(login_url='/login/')
def homeView(request):
    return render(request, "home_page.html", {})


@login_required(login_url='/login/')
def dashboardView(request):
    return render(request, "dashboard.html", {})


@login_required(login_url='/login/')
def logoutUser(request):
    logout(request)
    return redirect('dashboard')


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

    return render(request, "login_page.html", context=context)


def signup(request):
    if request.method == "POST":
        user_name = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']

        new_user = User.objects.create_user(user_name, email, password)
        new_user.first_name = first_name
        new_user.last_name = last_name

        return redirect('/login/')

    return render(request, 'signup.html')

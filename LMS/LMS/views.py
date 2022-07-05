from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login


def homeView(request):
    return render(request, "home_page.html", {})

def dashboardView(request):
    return render(request, "dashboard.html", {})


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
            return render(request, "home_page.html", context)
        else:
            context["error"] = "Invalid username or password"
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

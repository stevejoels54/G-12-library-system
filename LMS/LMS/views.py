from django.shortcuts import render
from django.contrib.auth import authenticate, login


def homeView(request):
    return render(request, "homePage.html", {})


def loginView(request):
    context = {}
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        context["username"] = username
        context["password"] = password
        print(username, password)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return render(request, "homePage.html", context)
        else:
            context["error"] = "Invalid username or password"
            return render(request, "loginPage.html", context)

    return render(request, "loginPage.html", context=context)

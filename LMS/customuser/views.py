from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import CustomUser


@login_required(login_url='login')
def userProfile(request, pk):
    user = CustomUser.objects.get(id=pk)

    context = {'user': user}
    return render(request, 'customuser/profile_template.html', context)


@login_required(login_url='login/')
def userPayments(request):
    context = {'user': user}

    return render(request, 'customuser/payments_template.html', context)

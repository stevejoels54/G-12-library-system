from django.shortcuts import render

# Create your views here.
def bookView(request, *args, **kwargs):
    return render(request, 'books.html', {})

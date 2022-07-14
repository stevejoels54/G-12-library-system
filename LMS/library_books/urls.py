from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/<str:pk>/', views.dashboard, name='dashboard'),
    path('borrow_book/<str:book>/<str:pk>/',
         views.borrowBook,
         name='borrow_book'),
    path('searchbook', views.searchBook, name='searchbook'),
]

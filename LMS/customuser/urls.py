from django.urls import path
from . import views

urlpatterns = [
    path('user-profile/<str:pk>/', views.userProfile, name='profile'),
    path('user-payments/<str:pk>/', views.userPayments, name='payments'),
]

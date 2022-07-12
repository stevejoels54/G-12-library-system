from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/<str:pk>/', views.dashboard, name='dashboard'),
]

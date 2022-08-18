from django.urls import path
from . import views

urlpatterns = [
    path('user-profile/<str:pk>/', views.userProfile, name='profile'),
    path('user-payments/<str:pk>/', views.userPayments, name='payments'),
    path('user-notifications/<str:pk>/',
         views.userNotifications,
         name='notifications'),
    path('requestaction', views.requestAction, name='requestaction'),
]

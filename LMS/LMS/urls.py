from django.contrib import admin
from django.urls import path
from .views import homeView
from .views import loginView
from library_books.views import bookView
from .views import dashboardView
from .views import signup
from .views import logoutUser

urlpatterns = [
    path('admin/', admin.site.urls),

    path('login/', loginView, name='login'),
    path('signup/', signup, name="signup"),

    path('home/', homeView, name='home'),
    path('dashboard/', dashboardView, name='dashboard'),
    path('user-profile/<str:pk>/', dashboardView, name='dashboard'),
    path('book_info/', bookView, name='book_info'),
    path('dashboard/', dashboardView, name='dashboard'),
    path('signup/', signup, name="signup"),
    path('logout/', logoutUser, name="logout"),
]

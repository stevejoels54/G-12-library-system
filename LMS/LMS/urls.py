from django.contrib import admin
from django.urls import path, include
from .views import homeView, loginView, signup, logoutUser, home


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('customuser.urls')),
    path('', include('library_books.urls')),

    path('login/', loginView, name='login'),
    path('signup/', signup, name="signup"),
    path('home/', homeView, name='home'),
    path('logout/', logoutUser, name="logout"),
    path('', home, name="home"),
]

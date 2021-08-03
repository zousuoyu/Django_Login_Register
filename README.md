# Django project: User login and register system
### This is self-practice Django project
### This project built by following the instruction in: www.liujiangblog.com

## Brief user instruction:
* Build virtual environment
* Use pip to install all required libraries
* Make necessary modifications to 'settings.example.py' and change it to 'setting.py'
* run 'python manage.py migrate' in cmd
* run 'python manage.py runserver' to start the server

## url route settings
from django.contrib import admin
from django.urls import path, include
from login import views

urlpatterns = [

    path('admin/', admin.site.urls),
    path('index/', views.index),
    path('login/', views.login),
    path('register/', views.register),
    path('logout/', views.logout),
    path('captcha/', include('captcha.urls')),
    path('confirm/', views.user_confirm),

]
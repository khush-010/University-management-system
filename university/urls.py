"""
URL configuration for university project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from dashboard import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.start),
    path('home/',views.home,name='home'),
    path('login/',views.login,name='login'),
    path('signup/',views.signup,name='signup'),
    path('application/',views.application,name='application'),
    path('pen-applicatons/',views.pen_app,name='pen_app'),
    path('app-status/',views.app_status,name='app-status'),
    path('accept/',views.accept,name='accept'),
    path('reject/',views.reject,name='reject'),
    path('change-pass/',views.change_pass,name='change-pass'),
    path('forget-pass/',views.forget_pass,name='forget-pass'),
    path('confirm-otp/',views.confirm_otp,name="confirm-otp"),
    path('new-pass/',views.new_pass,name="new-pass"),
    path('logout/',views.logout,name='logout'),
]

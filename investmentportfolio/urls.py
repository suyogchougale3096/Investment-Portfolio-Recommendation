"""investmentportfolio URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from app1 import views

urlpatterns = [
    path('admin/',admin.site.urls),
    path('',views.landingpage,name="landingpage"),
    path('login/',views.user_login,name='login'),
    path('signup/',views.signup),
    path('warning/',views.warning,name="warning"),
    path('usernamewarning/',views.usernamewarning,name="usernamewarning"),
    path('home/', views.home, name='home'),
    path('logout/', views.user_logout, name='logout'),
    path('goal/',views.goal,name="goal"),
    path('imp/',views.imp,name="imp"),
    path('page1/',views.page1,name="page1"),
    path('page2/',views.page2,name="page2"),
    path('page3/',views.page3,name="page3"),
    path('page4/',views.page4,name="page4"),
    path('page5/',views.page5,name="page5"),
    path('index/', views.index, name='index'),
    path('investtypes/',views.investTypes,name='investTypes'),
    path('recommend/',views.recommend,name='recommend'),
    path('statergy/',views.statergy,name='statergy')
]

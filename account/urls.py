from django.shortcuts import render
from django.urls import path
from account import views


app_name = 'account'


urlpatterns = [
    path('registration/', views.register_user, name='registration'),
    path('email_verification_sent/',
         lambda request: render(request,'account/email/email_verification_sent.html'),
         name='email_verification_sent'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('dashboard/', views.dashboard_user, name='dashboard'),
    path('profile_management/', views.profile_user, name='profile_management'),
    path('delete_user', views.delete_user, name='delete_user'),
    ]

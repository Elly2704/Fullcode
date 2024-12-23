from django.shortcuts import render
from django.urls import path, reverse_lazy
from account import views
from django.contrib.auth import views as auth_views


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
    # Password reset
    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='account/password/password_reset.html',
        email_template_name='account/password/password_reset_email.html',
        success_url=reverse_lazy('account:password_reset_done')),
         name='password_reset'),

    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='account/password/password_reset_done.html'),
         name='password_reset_done'),

    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='account/password/password_reset_confirm.html',
        success_url=reverse_lazy('account:password_reset_complete')),
         name='password_reset_confirm'),

    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='account/password/password_reset_complete.html'),
         name='password_reset_complete'),

]



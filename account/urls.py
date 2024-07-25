from django.urls import path
from account import views


app_name = 'account'


urlpatterns = [
    path('registration/', views.register_user, name='registration'),
    path('email_verification/', views.email_verification, name='email_verification'),
    #path('login/', login_view, name='login'),
    #path('logout/', logout_view, name='logout'),
    #path('profile/', profile_view, name='profile'),
    ]

from django.urls import path
from .views import *

app_name = 'cart'


urlpatterns = [
    path('', cart_view, name='cart_view'),
    path('add/', cart_add, name='cart_add'),
    path('update/', cart_update, name='cart_update'),
    path('delete/', cart_delete, name='cart_delete'),
  ]
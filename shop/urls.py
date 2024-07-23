from django.urls import path
from .views import *

app_name = 'shop'


urlpatterns = [
    path('', products_view, name='products'),
    path('product/<slug:slug>/', products_detail_view, name='product_detail'),
    path('category/<slug:slug>/', category_list, name='category_list'),
    ]
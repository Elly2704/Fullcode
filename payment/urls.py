from django.urls import path
from . import views

app_name = 'payment'

urlpatterns = [
    path('payment_success/', views.payment_success, name='payment_success'),
    path('payment_fail/', views.payment_fail, name='payment_fail'),
    path('shipping/', views.shipping, name='shipping'),
    path('checkout/', views.checkout, name='checkout'),
    path('complete_order/', views.complete_order, name='complete_order'),
]

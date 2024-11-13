from django.urls import path
from . import views
from .webhook import stripe_webhook

app_name = 'payment'

urlpatterns = [
    path('payment_success/', views.payment_success, name='payment_success'),
    path('payment_fail/', views.payment_fail, name='payment_fail'),
    path('shipping/', views.shipping, name='shipping'),
    path('checkout/', views.checkout, name='checkout'),
    path('complete_order/', views.complete_order, name='complete_order'),
    path('webhook_stripe/', stripe_webhook, name='webhook_stripe'),
]


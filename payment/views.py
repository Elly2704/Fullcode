import uuid
from decimal import Decimal

import stripe
import weasyprint
from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.templatetags.static import static
from django.urls import reverse
from yookassa import Configuration, Payment

from cart.cart import Cart

from .forms import ShippingAddressForm
from .models import Order, OrderItem, ShippingAddress


@login_required(login_url='account:login')
def shipping(request):
    try:
        shipping_address = ShippingAddress.objects.get(user=request.user)
    except ShippingAddressForm.DoesNotExist:
        shipping_address = None
        
    form = ShippingAddressForm(instance=shipping_address)

    if request.method == 'POST':
        form = ShippingAddressForm(request.POST, instance=shipping_address)
        if form.is_valid():
            shipping_address = form.save(commit=False)
            shipping_address.user = request.user
            shipping_address.save()
            return redirect('account:dashboard')
    return render(request, 'shipping/shipping.html', {'form': form})



def checkout(request):
    #return render(request, 'checkout.html')
    pass


def complete_order(request):
    #return render(request, 'complete_order.html')
    pass


def payment_success(request):
    #return render(request, 'payment_success.html')
    pass


def payment_fail(request):
    #return render(request, 'payment_fail.html')
    pass

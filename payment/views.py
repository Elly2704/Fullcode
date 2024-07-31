import uuid
from decimal import Decimal

import stripe
import weasyprint
from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.templatetags.static import static
from django.urls import reverse


from cart.cart import Cart
from .forms import ShippingAddressForm
from .models import Order, OrderItem, ShippingAddress

stripe.api_key = settings.STRIPE_SECRET_KEY
stripe.api_version = settings.STRIPE_API_VERSION


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
    if request.user.is_authenticated:
        shipping_address = get_object_or_404(ShippingAddress, user=request.user)
        if shipping_address:
            return render(request, 'payment/checkout.html', {'shipping_address': shipping_address})
    return render(request, 'payment/checkout.html')


def complete_order(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        apartment_address = request.POST.get('apartment_address')
        street_address = request.POST.get('street_address')
        city = request.POST.get('city')
        country = request.POST.get('country')
        zip_code = request.POST.get('zip_code')

        cart = Cart(request)
        total_price = cart.get_total_price()

        shipping_address, _ = ShippingAddress.objects.get_or_create(
            user=request.user,
            defaults={
                'name': name,
                'email': email,
                'street_address': street_address,
                'apartment_address': apartment_address,
                'country': country,
                'zip': zip
            }
        )
        session_data = {
            'mode': 'payment',
            'success_url': request.build_absolute_uri(reverse('payment:payment_success')),
            'cancel_url': request.build_absolute_uri(reverse('payment:payment_fail')),
            'line_items': []

        }
        if request.user.is_authenticated():
            order = Order.objects.create(user=request.user, shipping_address=shipping_address, amount=total_price)
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity'],
                    user=request.user
                )
                session_data['line_items'].append({
                    'product_data': {
                        'id': str(uuid.uuid4()),
                        'name': item['product'].name,
                    },
                    'unit_amount': int(item['price'] * Decimal(100)),
                    'currency': 'USD',
                    'quantity': item['quantity'],
                }
                )
                session = stripe.checkout.Session.create(**session_data)
                return redirect(session.url, code=303)
        else:
            order = Order.objects.create(shipping_address=shipping_address, amount=total_price)
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity'],
                )
        return JsonResponse({'success': True})


def payment_success(request):
    for key in list(request.session.keys()):
        del request.session[key]
    return render(request, 'payment/payment_success.html')


def payment_fail(request):
    return render(request, 'payment/payment_fail.html')

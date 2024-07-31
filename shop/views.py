from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, ProductProxy


def products_view(request):
    products = ProductProxy.objects.all()
    return render(request, 'shop/products.html', {'products': products})


def products_detail_view(request, slug):
    product = get_object_or_404(ProductProxy, slug=slug)
    return render(request, 'shop/product_detail.html', {'product': product})


def category_list(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = ProductProxy.objects.select_related('category').filter(category=category)
    return render(request, 'shop/category_list.html', {'category': category, 'products': products})


def search_products(request):
    query = request.GET.get('q')
    products = ProductProxy.objects.filter(title__icontains=query).distinct()
    context = {'products': products}
    if not query or not products:
        return redirect('shop:products')
    return render(request, 'shop/products.html', context)

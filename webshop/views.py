from django.shortcuts import render, get_object_or_404
from .models import Category, Product

def list_products(request, id):
    category = get_object_or_404(Category, id=id)
    products = Product.objects.filter(category=category)
    return render(request, 'webshop/products.html', {'category': category, 'products': products})

def product_info(request, id):
    product = get_object_or_404(Product, id=id)
    images = product.images.all()
    return render(request, 'webshop/product.html', {'product': product, 'images': images})
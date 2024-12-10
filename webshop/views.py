from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Category, Product, CartItem

def list_products(request, id):
    category = get_object_or_404(Category, id=id)
    products = Product.objects.filter(category=category)
    return render(request, 'webshop/products.html', {'category': category, 'products': products})

def product_info(request, id):
    product = get_object_or_404(Product, id=id)
    images = product.images.all()
    return render(request, 'webshop/product.html', {'product': product, 'images': images})

# Cart
@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = CartItem.objects.get_or_create(
        user=request.user,
        product=product,
        defaults={'quantity': 1}
    )

    # If item has not been added for the first time
    if not created:
        cart_item.quantity += 1

    cart_item.save()
    return redirect('cart')

@login_required
def cart_detail(request):
    cart_items = CartItem.objects.filter(user=request.user)
    return render(request, 'webshop/cart.html', {'cart_items': cart_items})

@login_required
def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id)

    if cart_item.user == request.user:
        cart_item.delete()

    return redirect('cart')

@login_required
def update_cart_item(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id)

    if cart_item.user == request.user:
        quantity = int(request.POST.get('quantity', 1))

        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
        else:
            cart_item.delete()

    return redirect('cart')

@login_required
def checkout(request):
    return redirect('/')
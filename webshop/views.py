from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages

from .models import Category, Product, CartItem, Order, OrderItem
from account.models import Address

def list_products(request, id):
    category = get_object_or_404(Category, id=id)
    product_list = Product.objects.filter(category=category)
    
    # Pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(product_list, 10)

    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

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

    cart_item.save()
    return redirect('cart')

@login_required
def cart_detail(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_cost = sum(item.product.price * item.quantity for item in cart_items)
    return render(request, 'webshop/cart.html', {'cart_items': cart_items, 'total_cost': total_cost})

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
    cart_items = CartItem.objects.filter(user=request.user)    
    addresses = Address.objects.filter(user=request.user)
    total_price = sum(item.product.price * item.quantity for item in cart_items)

    if request.method == 'POST':
        address_id = request.POST.get('address')
        address = get_object_or_404(Address, id=address_id, user=request.user)

        # Check if all products are available
        for item in cart_items:
            if item.product.stock < item.quantity:
                messages.error(request, f"Not enough stock for {item.product.name}. Only {item.product.stock} left.")
                return redirect('cart')

        # Create a new order
        order = Order.objects.create(user=request.user)

        # Add items to a new order
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )

            # Deduct stock from the product
            product.stock -= item.quantity
            product.save()

        cart_items.delete()
        return redirect('order_confirmation', order_id=order.id)
    
    return render(request, 'webshop/checkout.html', {'cart_items': cart_items, 'addresses': addresses, 'total_price': total_price})

@login_required
def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    order_items = order.orderitem_set.all()
    total_price = order.get_total_price()
    return render(request, 'webshop/order_confirmation.html', {'order': order, 'order_items': order_items, 'total_price': total_price})

@login_required
def orders(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'webshop/orders.html', {'orders': orders})
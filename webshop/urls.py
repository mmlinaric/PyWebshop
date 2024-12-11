from django.urls import path
from . import views

urlpatterns = [
    path('category/<int:id>', views.list_products, name='list-products'),
    path('product/<int:id>', views.product_info, name='product'),
    path('checkout/', views.checkout, name='checkout'),
    path('order_confirmation/<int:order_id>', views.order_confirmation, name='order_confirmation'),
    path('orders', views.orders, name='orders'),
 
    # Cart
    path('cart/', views.cart_detail, name='cart'),
    path('cart/add/<int:product_id>', views.add_to_cart, name='add-to-cart'),
    path('cart/remove/<int:cart_item_id>', views.remove_from_cart, name='remove-from-cart'),
    path('cart/update/<int:cart_item_id>', views.update_cart_item, name='update-cart-item'),
]
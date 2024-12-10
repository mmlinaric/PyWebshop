from django.urls import path
from . import views

urlpatterns = [
    path('category/<int:id>', views.list_products, name='list-products'),
    path('product/<int:id>', views.product_info, name='product'),
]
from django.urls import path

from . import views

urlpatterns = [
    path('register', views.UserRegistrationView.as_view(), name='register'),
    path('addresses', views.address_list, name='address-list'),
    path('addresses/add', views.add_address, name='add-address'),
    path('addresses/edit/<int:address_id>', views.edit_address, name='edit-address'),
    path('addresses/delete/<int:address_id>', views.delete_address, name='delete-address'),
]
from django.shortcuts import redirect, render
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required

from .forms import UserRegistrationForm, UserAddressForm
from .models import Address

class UserRegistrationView(SuccessMessageMixin, CreateView):
    template_name = "registration/register.html"
    success_url = reverse_lazy('login')
    form_class = UserRegistrationForm
    success_message = "You have registered successfully."

@login_required
def address_list(request):
    addresses = Address.objects.filter(user=request.user)
    return render(request, 'address/addresses.html', {'addresses': addresses})

@login_required
def add_address(request):
    if request.method == 'POST':
        form = UserAddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            return redirect('address-list')
    else:
        form = UserAddressForm()

    return render(request, 'address/add_address.html', {'form': form})

@login_required
def edit_address(request, address_id):
    address = Address.objects.get(id=address_id, user=request.user)

    if request.method == 'POST':
        form = UserAddressForm(request.POST, instance=address)
        if form.is_valid():
            address = form.save()
            return redirect('address-list')
    else:
        form = UserAddressForm(instance=address)

    return render(request, 'address/edit_address.html', {'form': form})

@login_required
def delete_address(request, address_id):
    address = Address.objects.get(id=address_id, user=request.user)
    address.delete()
    return redirect('address-list')
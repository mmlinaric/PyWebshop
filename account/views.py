from django.shortcuts import render
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .forms import UserRegistrationForm

class UserRegistrationView(SuccessMessageMixin, CreateView):
    template_name = "registration/register.html"
    success_url = reverse_lazy('login')
    form_class = UserRegistrationForm
    success_message = "You have registered successfully."
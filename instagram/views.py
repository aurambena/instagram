from django.shortcuts import render
from django.contrib.auth.models import User
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .forms import AccountForm
from django.contrib import messages

class HomeView(TemplateView):
    template_name = "general/home.html"


class LoginView(TemplateView):
    template_name = "general/login.html"


class LegalView(TemplateView):
    template_name = "general/legal.html"


class ContactView(TemplateView):
    template_name = "general/contact.html"


class RegisterView(CreateView):
      model = User
      template_name = 'general/register.html'
      success_url = reverse_lazy('login')
      form_class= AccountForm

      def form_valid(self, form):
          messages.add_message(self.request, messages.SUCCESS, "User created successfully")
          return super(RegisterView, self).form_valid(form)
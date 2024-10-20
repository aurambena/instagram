from django.shortcuts import render
from django.views.generic import TemplateView

class HomeView(TemplateView):
    template_name = "general/home.html"


class LoginView(TemplateView):
    template_name = "general/login.html"


class RegisterView(TemplateView):
    template_name = "general/register.html"


class LegalView(TemplateView):
    template_name = "general/legal.html"


class ContactView(TemplateView):
    template_name = "general/contact.html"
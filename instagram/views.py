from django.shortcuts import render
from django.contrib.auth.models import User
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from .forms import AccountForm
from django.contrib import messages
from .forms import LoginForm
from django.views.generic.edit import FormView
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect


class HomeView(TemplateView):
    template_name = "general/home.html"


class LoginView(FormView):
    template_name = "general/login.html"
    form_class = LoginForm

    def form_valid(self, form):
        user = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=user, password=password)

        if user is not None:
            login(self.request, user)
            messages.add_message(self.request, messages.SUCCESS, f'Wellcome back {user.username}')
            return HttpResponseRedirect(reverse('home'))
        else:
            messages.add_message(
                self.request, messages.ERROR, ('User not registered or wrong password'))
            return super(LoginView, self).form_invalid(form)

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

def logout_view(request):
    logout(request)
    messages.add_message(request, messages.INFO, "Logout successfully")
    return HttpResponseRedirect(reverse('home'))
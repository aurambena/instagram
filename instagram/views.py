from django.shortcuts import render
from django.contrib.auth.models import User
from django.views.generic import TemplateView, DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy, reverse
from .forms import AccountForm
from django.contrib import messages
from .forms import LoginForm
from .forms import ProfileFollow
from django.views.generic.edit import FormView
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from profiles.models import UserProfile
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from posts.models import UserPost, PostComment
from profiles.models import Follow


class HomeView(TemplateView):
    template_name = "general/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # if User is logged
        if self.request.user.is_authenticated:
            followed = Follow.objects.filter(follower=self.request.user.profile).values_list('following__user', flat=True)
            # Query set to filter posts from people we follow
            last_posts = UserPost.objects.filter(user__profile__user__in=followed)

        else:
            last_posts= UserPost.objects.all().order_by('-created_at')[:5]
        
        context['last_posts'] = last_posts
        
        return context

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

@method_decorator(login_required, name='dispatch')
class ProfileUpdateView(UpdateView):
    model = UserProfile
    template_name = 'general/edit_profile.html'
    context_object_name = 'profile'
    fields = ['bio', 'birth_date', 'profile_picture']

    def dispatch(self, request, *args, **kwargs):
        user_profile = self.get_object()
        if user_profile.user != self.request.user:
            return HttpResponseRedirect(reverse('home'))
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
          messages.add_message(self.request, messages.SUCCESS, "Profile updated successfully")
          return super(ProfileUpdateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('profile_detail', args=[self.object.pk])

@method_decorator(login_required, name='dispatch')
class ProfileDetailView(DetailView, FormView):
    model = UserProfile
    template_name = "general/profile_detail.html"
    context_object_name = 'profile'
    form_class = ProfileFollow

    def get_initial(self):
        self.initial['profile_pk'] =  self.get_object().pk
        return super().get_initial()

    def form_valid(self, form):
        profile_pk = form.cleaned_data.get('profile_pk')
        action = form.cleaned_data.get('action')
        following = UserProfile.objects.get(pk=profile_pk)
        
        if Follow.objects.filter(
            follower=self.request.user.profile,
            following=following
        ).count():
            Follow.objects.filter(
                follower=self.request.user.profile,
                following=following
            ).delete()
            messages.add_message(self.request, messages.SUCCESS, "User successfully unfollowed")

        else:
            Follow.objects.get_or_create(
                follower=self.request.user.profile,
                following=following
            )
            messages.add_message(self.request, messages.SUCCESS, "User successfully followed")
        return super().form_valid(form)

        # if action == 'follow':
        #   Follow.objects.get_or_create(
        #       follower = self.request.user.profile,
        #       following = following
        #   )
        #   messages.add_message(self.request, messages.SUCCESS, "User successfully followed")

        # elif action == 'unfollow':
        #    Follow.objects.filter(
        #       follower = self.request.user.profile,
        #       following = following
        #   ).delete()
        #    messages.add_message(self.request, messages.SUCCESS, "User successfully unfollowed")
        # return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('profile_detail', args=[self.request.user.profile.pk])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        following = Follow.objects.filter(follower=self.request.user.profile, following=self.get_object()).exists()
        context['following'] = following
        return context
    
@method_decorator(login_required, name='dispatch')
class ProfileListView(ListView):
    model = UserProfile
    template_name = "general/profiles_lists.html"
    context_object_name = 'profiles'

    def get_queryset(self):
        return UserProfile.objects.all().exclude(user=self.request.user)

@login_required
def logout_view(request):
    logout(request)
    messages.add_message(request, messages.INFO, "Logout successfully")
    return HttpResponseRedirect(reverse('home'))
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from posts.models import UserPost
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.contrib import messages


@method_decorator(login_required, name='dispatch')
class CreatePost(CreateView):
      model = UserPost
      fields = [
          'user', 
          'caption', 
          
          ]
      template_name = 'post/new_post.html'

      success_url = reverse_lazy('posts:new_post')

      def form_valid(self, form):
          messages.success(self.request, f'Post successfully created')
          form.instance.created_by = self.request.user
          return super().form_valid(form)
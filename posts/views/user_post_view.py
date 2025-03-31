from django.views.generic.edit import CreateView, UpdateView, DeleteView
from posts.models import UserPost
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.contrib import messages
from posts.forms import CreatePostForm
from django.views.generic.detail import DetailView
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.http import JsonResponse

@method_decorator(login_required, name='dispatch')
class CreatePost(CreateView):
      model = UserPost
      template_name = 'post/new_post.html'
      form_class= CreatePostForm

      success_url = reverse_lazy('home')

      def form_valid(self, form):
          messages.success(self.request, f'Post successfully created')
          form.instance.user = self.request.user
          return super().form_valid(form)   
      
@method_decorator(login_required, name='dispatch')
class PostDetailView(DetailView):
      model = UserPost
      template_name = 'general/post_detail.html'
      context_object_name = 'post'

@login_required
def like_post(request, pk):
      post = UserPost.objects.get(pk=pk)
      if request.user in post.likes.all():
          post.likes.remove(request.user)
          messages.add_message(request, messages.INFO, "I dont like it anymore")
      else:
          post.likes.add(request.user)
          messages.add_message(request, messages.INFO, "I like it")
      return HttpResponseRedirect(reverse('post_detail', args=[pk]))

@login_required
def like_post_ajax(request, pk):
      post = UserPost.objects.get(pk=pk)
      if request.user in post.likes.all():
          post.likes.remove(request.user)
          return JsonResponse(
               {
                    'message': 'I dont like it anymore',
                    'like': False,
                    'nLikes': post.likes.all().count()
               }
          )
      else:
          post.likes.add(request.user)
          return JsonResponse(
               {
                    'message': 'I like it',
                    'like': True,
                    'nLikes': post.likes.all().count()
               }
          )
          
from django.urls import path

from posts.views import(
    CreatePost,
    
)

app_name= 'posts'
urlpatterns = [
    path('post', CreatePost.as_view(), name='post'),

]

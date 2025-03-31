from django.db import models
from django.contrib.auth.models import User

class UserPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts', verbose_name='user')
    post_image = models.ImageField(upload_to='posts/', verbose_name='image')
    caption = models.TextField(max_length=500, blank=True, verbose_name='description')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='date')
    likes = models.ManyToManyField(User, related_name='post_likes', blank=True, verbose_name='likes')

    # Sets how names will appear in the admin
    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

    def __str__(self):
        return f"{self.user.username} - {self.created_at}"


class PostComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment')
    post = models.ForeignKey(UserPost, on_delete=models.CASCADE, related_name='comment')
    comment = models.TextField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # Sets how names will appear in the admin
    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'

    def __str__(self):
        return f"Commented by {self.user.username} about {self.post}"
    


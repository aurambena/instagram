from django.contrib import admin
from posts.models import UserPost, PostComment

@admin.register(UserPost)
class UserPostAdmin(admin.ModelAdmin):
    model = UserPost
    list_display = ('user', 'caption', 'created_at')

@admin.register(PostComment)
class UserPostComment(admin.ModelAdmin):
    model = PostComment
    list_display = ('user', 'post', 'comment', 'created_at')

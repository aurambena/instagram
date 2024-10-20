from django.contrib import admin
from .models import UserProfile, Follow

# Register your models here.

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    model = UserProfile
    list_display = ('user', 'profile_picture', 'bio', 'birth_date')

@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    model = Follow
    list_display = ('follower', 'following', 'created_at')

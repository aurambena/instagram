from django.contrib import admin
from .models import UserProfile 

# Register your models here.

@admin.register(UserProfile)
class PostResource(admin.ModelAdmin):
    model = UserProfile
    list_display = ('user', 'profile_picture', 'bio', 'birth_date')
    
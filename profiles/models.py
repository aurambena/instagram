from django.db import models
from django.contrib.auth.models import User

# This model structures a profile that is attached to the normal user and what the user will have
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True)
    birth_date = models.DateField('Birth date', null=True, blank=True)
    # followers = models.ManyToManyField('self', symmetrical=False, related_name='following', through='follow')

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'

    def __str__(self):
        return self.username
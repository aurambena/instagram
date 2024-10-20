from django.db import models
from django.contrib.auth.models import User

# This model structures a profile that is attached to the normal user and what the user will have
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True)
    birth_date = models.DateField('Birth date', null=True, blank=True)
    followers = models.ManyToManyField('self', symmetrical=False, related_name='following', through='follow')

    # Sets how names will appear in the admin
    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'

    def __str__(self):
        return self.username
    

# This model structures a follower-following unique relation and sets the date of this interaction
class Follow(models.Model):
    follower = models.ForeignKey(UserProfile, verbose_name='¿who is following?', on_delete=models.CASCADE, related_name='follower_set')
    following = models.ForeignKey(UserProfile, verbose_name='¿to who is following?', on_delete=models.CASCADE, related_name='following_set')
    created_at = models.DateField(auto_now_add=True, verbose_name='Since when is following')

    # Sets one interation
    class Meta:
        unique_together = ('follower', 'following')

    def __str__(self):
        return f"{self.follower} follows {self.following}"
    
    # Sets how names will appear in the admin
    class Meta:
        verbose_name = 'Folower'
        verbose_name_plural = 'Followers'
from django import forms
from .models import UserPost

class CreatePostForm(forms.ModelForm):
    class Meta:
        model = UserPost
        fields = [
          'post_image',
          'caption'
        ]
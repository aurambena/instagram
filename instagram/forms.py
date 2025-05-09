from django import forms
from django.contrib.auth.models import User

class AccountForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'password'

        ]

    def save(self):
        user = super().save(commit=True)
        user.set_password(self.cleaned_data["password"])
        user.save()

        from profiles.models import UserProfile
        UserProfile.objects.create(user=user)

        return user
    

class LoginForm(forms.Form):
    username = forms.CharField(max_length=140, label='username')
    password = forms.CharField( label='password', widget=forms.PasswordInput())

class ProfileFollow(forms.Form):
    profile_pk = forms.IntegerField(label='User Identification', widget=forms.HiddenInput())
    # action = forms.CharField(widget=forms.HiddenInput())
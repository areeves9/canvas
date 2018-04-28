from django import forms

from django.contrib.auth.models import User
from django.contrib.auth.forms import User, UserCreationForm
from accounts.models import Profile


class UserForm(forms.ModelForm):
    # email = forms.EmailField(max_length=200, help_text='Required')
    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "email",
        )


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = (
            "bio",
            "location",
            "birthdate",
            "photo",
        )


class UserRegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name',)

from django import forms

from django.contrib.auth.models import User
from accounts.models import Profile

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "email",
        ]

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            "bio",
            "location",
            "birthdate",
            "photo",
        ]

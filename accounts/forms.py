from django import forms

from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from accounts.models import Profile


class UserForm(forms.ModelForm):
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
        widgets = {
            'birthdate': forms.NumberInput(attrs={'type': 'date'}),
        }


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Password'}))

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['password'].label = ''
        self.fields['username'].label = ''


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email')
        labels = {
            'username': '',
            'email': '',
        }
        help_texts = {
            'username': None
        }
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Username'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email', 'required': 'required'}),
        }

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget = forms.PasswordInput(attrs={'placeholder': 'Password'})
        self.fields['password2'].widget = forms.PasswordInput(attrs={'placeholder': 'Password Confirmation'})
        self.fields['password1'].label = ''
        self.fields['password2'].label = ''

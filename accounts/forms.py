from django import forms

from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from accounts.models import Profile

from django.core.exceptions import ValidationError


class UserForm(forms.ModelForm):
    """A form to edit a User instance."""

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "email",
        )


class ProfileForm(forms.ModelForm):
    """A form to edit a Profile instance."""

    class Meta:
        model = Profile
        fields = (
            "bio",
            "location",
            "birthdate",
            "photo",
        )
        widgets = {
            "birthdate": forms.NumberInput(attrs={"type": "date"}),
        }


class LoginForm(AuthenticationForm):
    """A form for a user to log in."""

    username = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Username"})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Password"})
    )

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields["password"].label = ""
        self.fields["username"].label = ""


class UserRegisterForm(UserCreationForm):
    """A form for creating a new User instance."""

    class Meta:
        """UserRegistrationForm Meta class."""

        model = User
        fields = ("username", "email")
        labels = {
            "username": "",
            "email": "",
        }
        help_texts = {"username": None}
        widgets = {
            "username": forms.TextInput(attrs={"placeholder": "Username"}),
            "email": forms.EmailInput(
                attrs={"placeholder": "Email", "required": "required"}
            ),
        }

    def clean_username(self):
        """Raise ValidtionError if the provided username already exists."""
        username = self.cleaned_data["username"]
        if User.objects.filter(username=username).exists():
            raise ValidationError("Username already exists.")
        return username

    def __init__(self, *args, **kwargs):
        """Extend UserRegistrationForm.__init__"""
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        self.fields["password1"].widget = forms.PasswordInput(
            attrs={"placeholder": "Password"}
        )
        self.fields["password2"].widget = forms.PasswordInput(
            attrs={"placeholder": "Password Confirmation"}
        )
        self.fields["password1"].label = ""
        self.fields["password2"].label = ""

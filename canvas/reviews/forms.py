from django import forms

from django.contrib.auth.models import User
from accounts.models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = [
            "title",
            "strain",
            "method",
            "content",
            "photo",
        ]

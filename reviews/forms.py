from django import forms
from django.utils.text import slugify
from django.contrib.auth.models import User
from reviews.models import Review, Comment

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = [
            "title",
            "method",
            "content",
            "photo",
            "rating",
        ]

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = [
            "body"
        ]

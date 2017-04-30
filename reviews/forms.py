from django import forms

from django.contrib.auth.models import User
from reviews.models import Review

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
        # widgets = {
        #     "content": Textarea(attrs={"cols": 40, "rows": 15}),
        # }

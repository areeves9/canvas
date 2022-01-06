from django import forms
from django.utils.text import slugify

# from django_starfield import Stars

from reviews.models import Review, Comment
from reviews.widgets import MethodSelectWidget
from .widgets import FlavorSelectWidget


class ShareReviewForm(forms.Form):
    send_to = forms.EmailField()
    subject = forms.CharField(max_length=90)

    class Meta:
        fields = ["send_to", "subject"]
    pass


class ReviewForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)
        self.fields['rating'].label = ""

    photo = forms.ImageField(required=True)

    class Meta:
        model = Review
        fields = [
            "content",
            "flavors",
            "method",
            "photo",
            "rating",
            "title",
        ]
        labels = {
            'content': '',
            'method': '',
            'title': '',
        }
        help_texts = {
            'method': 'Choose method of consumption',
        }
        widgets = {
            'content': forms.Textarea(attrs={'placeholder': 'Description'}),
            'flavors': FlavorSelectWidget(),
            'method': MethodSelectWidget(attrs={'class': 'btn-group btn-group-toggle mb-3'}),
            'title': forms.TextInput(attrs={'placeholder': 'Title'}),
        }

    def save(self):
        instance = super(ReviewForm, self).save(commit=False)
        instance.slug = slugify(instance.title)

        return instance


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = [
            "body"
        ]

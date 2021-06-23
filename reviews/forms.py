from django import forms
from django.utils.text import slugify

from django_starfield import Stars

from reviews.models import Review, Comment
from reviews.widgets import MethodSelectWidget


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
    rating = forms.IntegerField(widget=Stars, required=True)

    class Meta:
        model = Review
        fields = [
            "rating",
            "title",
            "method",
            "content",
            "photo",
        ]
        labels = {
            'content': '',
            'method': '',
            'rating': '',
            'title': '',
        }
        help_texts = {
            'method': 'Choose method of consumption'
        }
        widgets = {
            'content': forms.Textarea(attrs={'placeholder': 'Description'}),
            'method': MethodSelectWidget(attrs={'class': 'btn-group btn-group-toggle mb-3'}),
            'title': forms.TextInput(attrs={'placeholder': 'Title'}),
        }

    def save(self):
        instance = super(ReviewForm, self).save(commit=False)
        instance.slug = slugify(instance.title)
        instance.save()

        return instance


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = [
            "body"
        ]

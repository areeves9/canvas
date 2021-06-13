from django import forms
from django.utils.text import slugify

from django_starfield import Stars

from reviews.models import Review, Comment


class ShareReviewForm(forms.Form):
    send_to = forms.EmailField()
    subject = forms.CharField(max_length=90)

    class Meta:
        fields = ["send_to", "subject"]
    pass


class ReviewForm(forms.ModelForm):
    photo = forms.ImageField(
        required=True,
    )
    rating = forms.IntegerField(widget=Stars)
    method = forms.ChoiceField(),

    class Meta:
        model = Review
        fields = [
            "title",
            "method",
            "content",
            "photo",
            "rating",
        ]
        labels = {
            'title': '',
            'content': '',
            'method': '',
        }
        help_texts = {
            'method': 'Choose method of consumption'
        }
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Title'}),
            'content': forms.Textarea(attrs={'placeholder': 'Description'}),
            'method': forms.RadioSelect(),
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

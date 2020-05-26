from django import forms
from django.utils.text import slugify
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

    class Meta:
        model = Review
        fields = [
            "title",
            "method",
            "content",
            "photo",
            "rating",
        ]

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

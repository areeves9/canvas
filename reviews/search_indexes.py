from haystack import indexes
from reviews.models import Review


class ReviewIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(
        document=True,
        use_template=True,
        template_name="search/indexes/reviews/review_text.txt"
    )
    title = indexes.CharField(model_attr='title')
    content = indexes.CharField(model_attr='content')

    def get_model(self):
        return Review

    def index_queryset(self, using=None):
        return self.get_model().objects.all()

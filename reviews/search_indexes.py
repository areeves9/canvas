from haystack import indexes
from reviews.models import Review, Strain


class ReviewIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(
        document=True,
        use_template=True,
        template_name="search/indexes/reviews/review_text.txt"
    )
    title = indexes.CharField(model_attr='title', defaul='', null=True)
    content = indexes.CharField(model_attr='content', default='', null=True)
    user = indexes.CharField(model_attr='user', default='', null=True)

    def get_model(self):
        return Review

    def index_queryset(self, using=None):
        return self.get_model().objects.all()


class StrainIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(
        document=True,
        use_template=True,
        template_name="search/indexes/reviews/strain_text.txt"
    )
    name = indexes.CharField(model_attr='name', default='', null=True)
    summary = indexes.CharField(model_attr='summary', default='', null=True)

    def get_model(self):
        return Strain

    def index_queryset(self, using=None):
        return self.get_model().objects.all()

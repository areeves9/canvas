from django.urls import reverse, resolve


class TestUrls:
    def test_reviews_url(self):
        path = reverse('reviews:reviews')
        assert resolve(path).view_name == 'reviews:reviews'

    def test_review_detail_url(self):
        path = reverse('reviews:review_detail', kwargs={'id': 1})
        assert resolve(path).view_name == 'reviews:review_detail'

    def test_strain_reviews_url(self):
        path = reverse('reviews:strain_reviews', kwargs={'id': 3})
        assert resolve(path).view_name == 'reviews:strain_reviews'

    def test_strains_url(self):
        path = reverse('reviews:strains')
        assert resolve(path).view_name == 'reviews:strains'

    def test_strain_detail_url(self):
        path = reverse('reviews:strain_detail', kwargs={'id': 3})
        assert resolve(path).view_name == 'reviews:strain_detail'

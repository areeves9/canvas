from django.test import RequestFactory
from django.urls import reverse, reverse_lazy
from django.contrib.auth.models import User,AnonymousUser
from reviews.models import Strain
from reviews.views import reviews, strains, strain_review
from mixer.backend.django import mixer
import pytest


@pytest.mark.django_db
class TestViews:
    def test_reviews_authenticated(self):
        path = reverse('reviews:reviews')
        request = RequestFactory().get(path)
        request.user = mixer.blend(User)
        response = reviews(request)
        assert response.status_code == 200

    def test_reviews_not_authenticated(self):
        path = reverse('reviews:reviews')
        request = RequestFactory().get(path)
        request.user = AnonymousUser()
        
        response = reviews(request)
        assert '/?next=/reviews/' in response.url

    def test_strains_authenticated(self):
        path = reverse('reviews:strains')
        request = RequestFactory().get(path)
        request.user = mixer.blend(User)
        response = strains(request)
        assert response.status_code == 200

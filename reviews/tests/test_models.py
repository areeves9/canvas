from mixer.backend.django import mixer
from reviews.models import Strain, Review
from reviews.views import strain_detail
from django.contrib.auth.models import User
from django.urls import reverse, resolve
from django.test import RequestFactory

import pytest


@pytest.fixture
def factory():
    return RequestFactory()


@pytest.fixture
def strain(request, db):
    return mixer.blend(
        Strain,
        photo_url='http://www.cannabisreports.com/images/strains/no_image.png'
    )


@pytest.mark.django_db
class TestModels:
    def test_get_average_rating(self, strain):
        user = mixer.blend(User)
        reviews = mixer.cycle(10).blend(
            Review,
            strain=strain,
            user=user,
            rating=mixer.RANDOM
            )
        strain.user_review.set(reviews)
        assert strain.get_average_rating() > 0

    def test_get_non_rating(self, strain):
        assert strain.get_average_rating() == "No ratings"

    def test_get_absolute_strain_url(self, strain, factory, db):
        path = strain.get_absolute_url()
        assert resolve(path).view_name == 'reviews:strain_detail'

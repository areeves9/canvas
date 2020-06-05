import pytest
from django.views.generic.edit import CreateView

from django.contrib.auth import login, logout
from django.contrib.auth.models import User, AnonymousUser

from django.urls import reverse, reverse_lazy
from django.test import RequestFactory, Client

from accounts.views import profile, RegistrationView
from mixer.backend.django import mixer


@pytest.mark.django_db
class TestViews:
    def test_user_login(self):
        path = reverse('home')
        client = Client()
        request = RequestFactory().get(path)
        request.session = client.session
        request.user = mixer.blend(User)

        login(request=request, user=request.user)
        assert request.user.is_authenticated

    def test_user_logout(self):
        path = reverse('accounts:logout')
        client = Client()
        request = RequestFactory().get(path)
        request.session = client.session
        request.user = mixer.blend(User)

        logout(request=request)
        assert not request.user.is_authenticated

    def test_create_user(self):
        path = reverse('accounts:register')
        client = Client()
        request = RequestFactory().get(path)
        request.session = client.session
        request.user = mixer.blend(User)

        response = RegistrationView(request=request)
        assert reverse('reviews:reviews') in response.success_url

    def test_profile_authenticated(self):
        path = reverse('accounts:profile')
        request = RequestFactory().get(path)
        request.user = mixer.blend(User)

        response = profile(request=request)
        assert response.status_code == 200

    def test_profile_not_authenticated(self):
        path = reverse('accounts:profile')
        client = Client()
        request = RequestFactory().get(path)
        request.user = AnonymousUser()
        request.session = client.session

        response = profile(request=request)
        assert response.url == '/?next=/accounts/profile/'

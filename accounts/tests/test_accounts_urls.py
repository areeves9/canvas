from django.urls import reverse, resolve


class TestUrls:
    def test_registration_url(self):
        path = reverse('accounts:register')
        assert resolve(path).view_name == 'accounts:register'

    def test_logout_url(self):
        path = reverse('accounts:logout')
        assert resolve(path).view_name == 'accounts:logout'

    def test_password_change_url(self):
        path = reverse('accounts:password_change')
        assert resolve(path).view_name == 'accounts:password_change'

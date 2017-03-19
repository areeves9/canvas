from django.conf.urls import include, url
from django.contrib.auth.forms import UserCreationForm

from . import views
from django.views.generic.edit import CreateView

urlpatterns = [
    url(r'^register', CreateView.as_view(
        template_name='registration/registration_form.html',
        form_class=UserCreationForm,
        success_url='/accounts/login/',
    ), name='register'),
    url(r'^profile', views.profile, name='profile'),
]

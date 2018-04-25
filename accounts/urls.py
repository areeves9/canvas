from django.conf import settings
from django.conf.urls import include, url
from django.contrib.auth.forms import UserCreationForm

from . import views
from django.views.generic.edit import CreateView
from django.contrib.auth import views as auth_views


urlpatterns = [
    url(r'^register/$', CreateView.as_view(
        template_name='registration/registration_form.html',
        form_class=UserCreationForm,
        success_url='/accounts/login/',
    ), name='register'),
    url(r'^password_change/$', auth_views.password_change, {'template_name': 'registration/password_change.html','post_change_redirect': 'accounts:password_change_done'}, name="password_change"),
    url(r'^password_change/done/$', auth_views.password_change_done, {'template_name': 'registration/password_change_done.html'}, name='password_change_done'),
    url(r'^users/follow/$', views.user_follow, name='user_follow'),
    url(r'^users/$', views.users, name='users'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^profile/update/$', views.profile_update, name='update'),
    url(r'^profile/(?P<username>\w+)/$', views.profile_user, name='user'),
]

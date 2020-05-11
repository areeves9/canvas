from . import views
from django.conf import settings
from django.conf.urls import include, url
from django.urls import reverse
from accounts.forms import UserForm, UserRegisterForm
from django.views.generic.edit import CreateView
from django.contrib.auth import views as auth_views


urlpatterns = [
    url(r'^register/$', CreateView.as_view(
        template_name='registration/registration_form.html',
        form_class=UserRegisterForm,
        success_url='/account/login/',
    ), name='register'),
    url(r'^login/$', auth_views.login, {'template_name': 'registration/login.html'}, name="login"),
    url(r'^logout/$', auth_views.logout, {'template_name': 'registration/logged_out.html', 'next_page': '/'}, name="logout"),
    url(r'^password_change/$', auth_views.password_change, {'template_name': 'registration/password_change.html','post_change_redirect': 'accounts:password_change_done'}, name="password_change"),
    url(r'^password_change/done/$', auth_views.password_change_done, {'template_name': 'registration/password_change_done.html'}, name='password_change_done'),
    url(r'^password_reset/$', auth_views.password_reset, {'template_name': 'registration/password_reset.html'}, name='password_reset'),
    url(r'^password_reset/done/$', auth_views.password_reset_done, {'template_name': 'registration/password_reset_done.html'}, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.password_reset_confirm, name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),
    url(r'^users/follow/$', views.user_follow, name='user_follow'),
    url(r'^users/$', views.users, name='users'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^profile/update/$', views.profile_update, name='update'),
    url(r'^profile/(?P<username>\w+)/$', views.profile_user, name='user'),
    url(r'^actions/$', views.actions, name='actions')
]

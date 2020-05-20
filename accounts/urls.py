from . import views
from django.urls import re_path, reverse
from accounts.forms import UserRegisterForm
from django.views.generic.edit import CreateView
from django.contrib.messages.views import SuccessMessageMixin

from django.contrib.auth.views import (
    LogoutView,
    PasswordChangeView,
    PasswordChangeDoneView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)

app_name = 'accounts'

urlpatterns = [
    re_path(r'^register/$', CreateView.as_view(
                template_name='registration/registration_form.html',
                form_class=UserRegisterForm,
                success_url='/reviews/'
            ), name='register'),
    re_path(r'^logout/$', LogoutView.as_view(
                template_name='registration/logged_out.html',
                next_page='/'
            ), name='logout'),
    re_path(r'^password_change/$', PasswordChangeView.as_view(
                template_name='registration/password_change.html',
            ), name="password_change"),
    re_path(r'^password_change/done/$', PasswordChangeDoneView.as_view(
                template_name='registration/password_change_done.html'
            ), name='password_change_done'),
    re_path(r'^password_reset/$', PasswordResetView.as_view(
                template_name='registration/password_reset.html'
            ), name='password_reset'),
    re_path(r'^password_reset/done/$', PasswordResetDoneView.as_view(
                template_name='registration/password_reset_done.html',
            ), name='password_reset_done'),
    re_path(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
            PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    re_path(r'^reset/done/$', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    re_path(r'^users/follow/$', views.user_follow, name='user_follow'),
    re_path(r'^profile/$', views.profile, name='profile'),
    re_path(r'^profile/update/$', views.profile_update, name='update'),
    re_path(r'^profile/(?P<username>\w+)/$', views.profile_user, name='user'),
    re_path(r'^actions/$', views.actions, name='actions')
]

from . import views
from django.urls import path

from django.contrib.auth.views import (
    LogoutView,
    PasswordChangeView,
    PasswordChangeDoneView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)

app_name = "accounts"

urlpatterns = [
    path("register/", views.RegistrationView.as_view(), name="register"),
    path(
        "logout/",
        LogoutView.as_view(template_name="registration/logged_out.html", next_page="/"),
        name="logout",
    ),
    path(
        "password_change/",
        PasswordChangeView.as_view(
            template_name="registration/password_change.html",
        ),
        name="password_change",
    ),
    path(
        "password_change/done/",
        PasswordChangeDoneView.as_view(
            template_name="registration/password_change_done.html"
        ),
        name="password_change_done",
    ),
    path(
        "password_reset/",
        PasswordResetView.as_view(template_name="registration/password_reset.html"),
        name="password_reset",
    ),
    path(
        "password_reset/done/",
        PasswordResetDoneView.as_view(
            template_name="registration/password_reset_done.html",
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(
            template_name="registration/password_reset_confirm.html",
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        PasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
    path("users/follow/", views.user_follow, name="user_follow"),
    path("profile/", views.profile, name="profile"),
    path("profile/update/", views.profile_update, name="update"),
    path("profile/<username>/", views.profile_user, name="user"),
    path("actions/", views.actions, name="actions"),
]

from django.apps import AppConfig


class AccountsConfig(AppConfig):
    """Accounts app configuration."""

    name = "accounts"
    verbose_name = "Accounts"

    def ready(self):
        from accounts.signals import create_profile_user_post_save, profile_post_save

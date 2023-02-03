"""Signals for accounts.models."""

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from accounts.models import Profile


@receiver(post_save, sender=User)
def create_profile_user_post_save(sender, instance, created, **kwargs):
    """Create a Profile when a User is saved."""
    if created:
        profile = Profile.objects.create(user=instance)
        profile.save()


@receiver(post_save, sender=Profile)
def profile_post_save(sender, instance, **kwargs):
    """Run Profile.process_photo() before a Profile is saved."""
    instance.process_photo()

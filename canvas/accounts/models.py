from django.db import models

from django.conf import settings
from django.contrib.auth.models import User

from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bio = models.TextField(max_length=1000, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birthdate = models.DateField(null=True, blank=True)
    photo = models.ImageField(blank=True, null=True)

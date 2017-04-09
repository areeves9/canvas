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

def upload_location(instance, filename):
    return "%s/%s" % (instance.user, filename)

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bio = models.TextField(max_length=1000, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birthdate = models.DateField(null=True, blank=True)
    photo = models.ImageField(
        upload_to=upload_location,
        blank=True,
        null=True,
        height_field="height_field",
        width_field="width_field",
    )
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)

class Follow(models.Model):
    followed = models.ForeignKey(User, related_name='followed')
    following = models.ForeginKey(User, related_nam='following')
    created = models.DateTimeField(auto_now_add=True, db_index=True)

    def __str__(self):
        return '%s follows %s' % (self.following, self.followed)

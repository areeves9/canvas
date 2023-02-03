"""Models for canvas.accounts."""

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models

from common.tasks import process_photo_for_upload

# Create your models here.


def upload_location(instance, filename):
    """Set file path for upload."""
    return "%s/%s" % (instance.user, filename)


class Profile(models.Model):
    """A model with a one-to-one relationship with User."""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
    )
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
    width_field = models.IntegerField(default=0, null=True)
    height_field = models.IntegerField(default=0, null=True)

    def __str__(self):
        """Represent instance as a string."""
        return "Profile: {}".format(self.user)

    def process_photo(self):
        """Run task to rotate and resize photo before upload."""
        # if not self.id and not self.photo:
        process_photo_for_upload.delay(self.id)


class Follow(models.Model):
    """Table to relate two users in a follow relationship."""

    follow_from = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="follow_from"
    )
    follow_to = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="follow_to"
    )
    created = models.DateTimeField(auto_now_add=True, db_index=True)

    def __str__(self):
        """String representation of a Follow."""
        return "%s follows %s" % (self.follow_from, self.follow_to)


User.add_to_class(
    "following",
    models.ManyToManyField(
        "self", through=Follow, related_name="followers", symmetrical=False
    ),
)

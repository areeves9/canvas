import os

import requests
from django.conf import settings
from django.db import models
from django.db.models import JSONField
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from PIL import Image

# from common.tasks import process_photo_for_upload
from common.utils import image_compress, image_rotate
from strains.models import Flavor, Strain

# Create your models here.

# save key to environment variable
headers = {
    "X-API-Key": os.environ.get("CANNABIS_REPORTS_API"),
}


cannabis_reports_url = "https://www.cannabisreports.com/api/v1.0/strains/search/"
flag_api_url = "https://restcountries.eu/rest/v2/name/"


def upload_location(instance, filename):
    return "%s/%s" % (instance.user, filename)


def upload_location1(instance, filename):
    return "%s/%s" % (instance, filename)


class Review(models.Model):
    """User submitted review of a strain specific experience."""

    title = models.CharField(max_length=35)
    content = models.TextField(max_length=500)
    flavors = models.ManyToManyField(Flavor)
    strain = models.ForeignKey(
        Strain, on_delete=models.CASCADE, related_name="user_review"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="user_reviews",
        default=1,
    )
    photo = models.ImageField(
        upload_to=upload_location,
        blank=True,
        null=True,
        height_field="height_field",
        width_field="width_field",
    )
    height_field = models.IntegerField(default=0, null=True)
    width_field = models.IntegerField(default=0, null=True)
    FLOWER = "Flower"
    EXTRACT = "Extract"
    EDIBLE = "Edible"
    METHOD_CHOICES = (
        (FLOWER, "Flower"),
        (EXTRACT, "Extract"),
        (EDIBLE, "Edible"),
    )
    method = models.CharField(
        max_length=20, choices=METHOD_CHOICES, default="Flower", blank=False
    )
    RATING_CHOICES = (
        (1, "1"),
        (2, "2"),
        (3, "3"),
        (4, "4"),
        (5, "5"),
    )
    rating = models.IntegerField(choices=RATING_CHOICES, default=5)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    users_like = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="reviews_liked", blank=True
    )

    class Meta:
        """Meta class for Strain."""

        ordering = ["-timestamp", "-updated"]

    def get_flavors(self):
        """Get related flavors to a Strain."""
        return "\n".join([f.name for f in self.flavors.all()])

    def get_absolute_url(self):
        """Get absolute url of an instance."""
        return reverse("reviews:review_detail", kwargs={"pk": self.pk})

    def __str__(self):
        """String representation of a Review instance."""
        return self.title

    # def process_photo(self):
    #     """Run task to rotate and resize photo before upload."""
    #     if not self.id and not self.photo:
    #     process_photo_for_upload.delay(self.id)


@receiver(post_save, sender=Review)
def update_image(sender, instance, **kwargs):
    """Process the review photo."""
    if instance.photo:
        image = Image.open(instance.photo)
        return image_compress(image_rotate(image), instance)


class Comment(models.Model):
    """User created review comment."""

    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name="comments"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="user_comments",
        default=1,
    )
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ["created"]

    def __str__(self):
        return "{} commented on {}".format(self.user, self.review)

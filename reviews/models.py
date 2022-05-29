import os
import requests
from django.db import models
from django.db.models import JSONField
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save
from django.urls import reverse
from django.conf import settings

from PIL import Image

from common.utils import image_rotate, image_compress


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


class Flavor(models.Model):
    name = models.CharField(max_length=60, blank=False)

    def __str__(self):
        return self.name


class Strain(models.Model):
    name = models.CharField(max_length=60, unique=True, blank=False)
    summary = models.TextField(blank=True, null=True)
    lineage = JSONField(blank=True, null=True)
    genetics = JSONField(blank=True, null=True)
    photo = models.ImageField(
        upload_to=upload_location1,
        blank=True,
        null=True,
        height_field="height_field",
        width_field="width_field",
    )
    photo_url = models.URLField(null=True, blank=True)
    height_field = models.IntegerField(default=0, null=True)
    width_field = models.IntegerField(default=0, null=True)
    users_like = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="strains_liked", blank=True
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("reviews:strain_detail", kwargs={"pk": self.pk})

    def get_average_rating(self):
        strain_ratings = self.user_review.all()
        if len(strain_ratings) > 0:
            ratings = [strain.rating for strain in strain_ratings]
            average = sum(ratings) / len(ratings)
            rounded_average = round(average, 1)
            return rounded_average

    def get_strain_image(self):
        strain_query_url = cannabis_reports_url + "%s" % (self.name)
        if not self.photo_url:
            try:
                r = requests.get(strain_query_url, headers)
                r.raise_for_status()
                if r.status_code == 200:
                    response = r.json()  # json strain object
                    # if there is a 200 code, there will be a strain
                    # however it may not have an 'image'
                    image_url = response["data"][0]["image"]  # url property of object
                    genetics = response["data"][0]["genetics"]["names"]
                    lineage = response["data"][0]["lineage"]
                    self.photo_url = image_url
                    self.genetics = genetics
                    self.lineage = lineage
                    self.save()
                    return
                elif r.status_code != 200:
                    self.photo_url = (
                        "http://www.cannabisreports.com/images/strains/no_image.png"
                    )
                    self.genetics = False
                    self.lineage = False
                    self.save()
            except requests.exceptions.HTTPError as err:
                raise SystemExit(err)
            except requests.exceptions.ConnectionError as err:
                raise SystemExit(err)
            except requests.exceptions.Timeout as err:
                raise SystemExit(err)
            except requests.exceptions.RequestException as err:
                raise SystemExit(err)


@receiver(post_save, sender=Strain)
def save_strain_image(sender, instance, created, **kwargs):
    """
    Called when the new strain object is saved.
    """
    instance.get_strain_image()


class Review(models.Model):
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
        ordering = ["-timestamp", "-updated"]

    def get_flavors(self):
        return "\n".join([f.name for f in self.flavors.all()])

    def get_absolute_url(self):
        return reverse("reviews:review_detail", kwargs={"pk": self.pk})

    def __str__(self):
        return self.title


@receiver(post_save, sender=Review)
def update_image(sender, instance, **kwargs):
    if instance.photo:
        image = Image.open(instance.photo)
        return image_compress(image_rotate(image), instance)


class Comment(models.Model):
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

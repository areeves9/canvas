import os
import requests
from django.db import models
from django.db.models import JSONField
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.urls import reverse
from django.conf import settings


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
    """Flavor model."""

    name = models.CharField(max_length=60, blank=False)

    def __str__(self):
        """Return string represenation of instance."""
        return self.name


class Strain(models.Model):
    """Cannabis strain model."""

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
        """Return string represenation of instance."""
        return self.name

    def get_absolute_url(self):
        """Return url of instance."""
        return reverse("reviews:strain_detail", kwargs={"pk": self.pk})

    def get_average_rating(self):
        """Return average strain rating."""
        strain_ratings = self.user_review.all()
        if len(strain_ratings) > 0:
            ratings = [strain.rating for strain in strain_ratings]
            average = sum(ratings) / len(ratings)
            rounded_average = round(average, 1)
            return rounded_average

    def get_strain_image(self):
        """Get photo url from API."""
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
    """Called when the new strain object is saved."""
    instance.get_strain_image()

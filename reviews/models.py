import os
import requests
from PIL import Image
from django.db import models
from django.core.files import File
from django.core.urlresolvers import reverse
from django.contrib.postgres.fields import JSONField
from django.conf import settings
from django.utils import timezone

# Create your models here.

# save key to environment variable
headers = {
    'X-API-Key': os.environ.get('CANNABIS_REPORTS_API'),
}
cannabis_reports_url = "https://www.cannabisreports.com/api/v1.0/strains/search/"
flag_api_url = "https://restcountries.eu/rest/v2/name/"


def upload_location(instance, filename):
    return "%s/%s" % (instance.user, filename)


def upload_location1(instance, filename):
    return "%s/%s" % (instance, filename)


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

    def get_absolute_url(self):
        return reverse("reviews:strain", kwargs={"id": self.id})

    def get_average_rating(self):
        strain_ratings = self.user_review.all()
        l1 = []
        for x in strain_ratings:
            l1.append(x.rating)
            average = sum(l1)/len(l1)
            if not average:
                return "N/A"
            else:
                return int(average)

    def get_strain_image(self):
        if not self.photo_url:
            strain_query_url = cannabis_reports_url + "%s" % (self.name)
            r = requests.get(strain_query_url, headers)
            if r.status_code == 200:
                data = r.json()  # json strain object
                image_url = data['data'][0]['image']  # url property of object
                self.photo_url = image_url
                self.save()
                return self.photo_url
            else:
                return self.photo_url

    def get_strain_lineage(self):
        if not self.lineage or not self.genetics:
            strain_query_url = cannabis_reports_url + "%s" % (self.name)
            r = requests.get(strain_query_url, headers)
            if r.status_code == 200:
                data = r.json()  # json strain object
                lineage_json = data['data'][0]['lineage']  # lineage property of object
                genetics_json = data['data'][0]['genetics']['names']
                if len(lineage_json) == 0:
                    self.lineage = False
                else:
                    self.lineage = lineage_json
                self.genetics = genetics_json
                self.save()
                return self.lineage, self.genetics
            elif r.status_code != 200:
                return "No Data Present"
        else:
            return self.lineage, self.genetics

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]


class Review(models.Model):
    title = models.CharField(max_length=35)
    content = models.TextField(max_length=500)
    strain = models.ForeignKey(Strain, related_name="user_review")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="user",
        default=1
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
    FLOWER = 'FLOWER'
    EXTRACT = 'EXTRACT'
    EDIBLE = 'EDIBLE'
    METHOD_CHOICES = (
        (FLOWER, 'FLOWER'),
        (EXTRACT, 'EXTRACT'),
        (EDIBLE, 'EDIBLE'),
    )
    method = models.CharField(
        max_length=20,
        choices=METHOD_CHOICES,
        default='FLOWER',
        blank=False
    )
    RATING_CHOICES = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    )
    rating = models.IntegerField(choices=RATING_CHOICES, default=5)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    users_like = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="reviews_liked",
        blank=True
    )

    class Meta:
        ordering = ["-timestamp", "-updated"]

    def get_absolute_url(self):
        return reverse("reviews:detail", kwargs={"id": self.id})

    def __str__(self):
        return self.title


class Comment(models.Model):
    review = models.ForeignKey(Review, related_name='comments')
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="user_comments",
        default=1
    )
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ["created"]

    def __str__(self):
        return '{} commented on {}'.format(self.user, self.review)

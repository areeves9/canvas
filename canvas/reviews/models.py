from django.db import models
from django.core.urlresolvers import reverse
from django.conf import settings
from django.utils import timezone

# Create your models here.

def upload_location(instance, filename):
    return "%s/%s" % (instance.user, filename)

class Strain(models.Model):
    name = models.CharField(max_length=60)
    summary = models.TextField(blank=True, null=True)

    def get_absolute_url(self):
        return reverse("reviews:strain", kwargs={"id": self.id})

    def __str__(self):
        return self.name

class Review(models.Model):
    title = models.CharField(max_length=35)
    content = models.TextField(max_length=500)
    strain = models.ForeignKey(Strain)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,  related_name="user" ,default=1)
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
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    class Meta:
        ordering = ["-timestamp", "-updated"]

    def get_absolute_url(self):
        return reverse("reviews:detail", kwargs={"id": self.id})

    def __str__(self):
        return self.title

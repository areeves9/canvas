import os
import requests
from PIL import Image
from django.db import models
from django.core.files import File
from django.core.urlresolvers import reverse
from django.conf import settings
from django.utils import timezone

# Create your models here.

# save key to environment variable
headers = {
    'X-API-Key': '08dd8bf42f9ca621002213991f9ef5bf96fdd66a',
}

def upload_location(instance, filename):
    return "%s/%s" % (instance.user, filename)

def upload_location1(instance, filename):
    return "%s/%s" % (instance, filename)

class Strain(models.Model):
    name = models.CharField(max_length=60)
    summary = models.TextField(blank=True, null=True)
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

    def get_strain_image(self):
        if not self.photo_url:
            cannabis_reports_url = "https://www.cannabisreports.com/api/v1.0/strains/search/%s" % (self.name)
            r = requests.get(cannabis_reports_url, headers)
            if r.status_code == 200:
                data = r.json() # json strain object
                image_url = data['data'][0]['image'] # url property of object
                self.photo_url = image_url
                self.save()
                return self.photo_url
            # im = Image.open(requests.get(image_url, stream=True).raw) # open that url to get the image
                # size = (500, 500) # desired image dimensions
                # new_im = im.resize(size) # resize image
                # save_location =  ('reviews/static/reviews/images/%s.jpg') % (self.name) # set location to save image
                # im.save(save_location) # save image

                # self.photo.save(
                #     os.path.basename(save_location),
                #     File(open(os.path.dirname(save_location), 'rb'))
                # )
                # self.save()
                # return image_url
            # elif (r.status_code != 200) or (not self.photo_url):
            #     placehold = "http://placehold.it/500x500"
            #     return placehold
            else:
                return self.photo_url

    def __str__(self):
        return self.name

class Review(models.Model):
    title = models.CharField(max_length=35)
    content = models.TextField(max_length=500)
    strain = models.ForeignKey(Strain, related_name="user_review")
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
    users_like = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="reviews_liked", blank=True)

    class Meta:
        ordering = ["-timestamp", "-updated"]

    def get_absolute_url(self):
        return reverse("reviews:detail", kwargs={"id": self.id})

    def __str__(self):
        return self.title

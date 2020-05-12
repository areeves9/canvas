import os

from PIL import Image, ExifTags
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import pre_save, post_save
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
    

@receiver(pre_save, sender=Profile)
def update_image(sender, instance, **kwargs):
    # does the image exist?
    if instance.photo:
        # filepath to the image in media_production folder
        filepath = os.path.join(settings.MEDIA_URL, instance.photo.name)
        # open image at path with Pillow
        image = Image.open(filepath)

        if hasattr(image, '_getexif'):
            try:
                # iterate through the EXIF tags
                for orientation in ExifTags.TAGS.keys(): 
                    if ExifTags.TAGS[orientation] == 'Orientation': 
                        break
                # get image exif metadata        
                e = image._getexif()
                # check if e exists
                if e is not None:
                    # get dictionary of exif key-value pairs
                    try:
                        exif = dict(e.items())
                        if (exif[orientation]) == 3:
                            image = image.rotate(180)
                        elif (exif[orientation]) == 6:
                            image = image.rotate(270)
                        elif (exif[orientation]) == 8:
                            image = image.rotate(90)
                    except:
                        pass
                box = (50, 50, 100, 100)
                size = 512, 512
                image.crop(box)
                image.thumbnail(size)

                image.save()
                image.close()
            except IOError as err:
                print("I/O error: {0}".format(err))


class Follow(models.Model):
    follow_from = models.ForeignKey(User, related_name='follow_from')
    follow_to = models.ForeignKey(User, related_name='follow_to')
    created = models.DateTimeField(auto_now_add=True, db_index=True)

    def __str__(self):
        return '%s follows %s' % (self.following, self.followed)


User.add_to_class('following', models.ManyToManyField('self', through=Follow, related_name='followers', symmetrical=False))

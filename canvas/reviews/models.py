from django.db import models

# Create your models here.
class Strain(models.Model):
    name = models.CharField(max_length=60)
    summary = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Review(models.Model):
    title = models.CharField(max_length=35)
    content = models.TextField(max_length=500)
    photo = 

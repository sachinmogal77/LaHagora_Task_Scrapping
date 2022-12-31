from django.db import models

# Create your models here.
class Playstore (models.Model):
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=2083, default="", unique=True)
    summary = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    reviews = models.CharField(max_length=200)
    ratings= models.CharField(max_length=200)
    histogram=models.CharField(max_length=200)
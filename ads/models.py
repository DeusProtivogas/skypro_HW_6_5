
from django.db import models


class Ad(models.Model):
    name = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    price = models.IntegerField(default=0)
    description = models.CharField(max_length=1000)
    address = models.CharField(max_length=120)
    is_published = models.BooleanField(default=False)


class Category(models.Model):
    name = models.CharField(max_length=30)
from django.db import models

# Create your models here.
from user.models import User


class Category(models.Model):
    name = models.CharField(max_length=30)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name


class Ad(models.Model):
    name = models.CharField(max_length=100)
    # author = models.CharField(max_length=100)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.IntegerField(default=0)
    description = models.CharField(max_length=1000)
    address = models.CharField(max_length=120)
    is_published = models.BooleanField(default=False)

    image = models.ImageField(upload_to="logos/")
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Объявление"
        verbose_name_plural = "Объявления"
        ordering = ["-price"]

    def __str__(self):
        return self.name


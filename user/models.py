from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
from location.models import Location


# class User(models.Model):
class User(AbstractUser):
    MEMBER = "member"
    MODERATOR = "moderator"
    ADMIN = "admin"

    ROLES = [(MEMBER, "Пользователь"), (MODERATOR, "Модератор"), (ADMIN, "Админ")]

    # first_name = models.CharField(max_length=20)
    # last_name = models.CharField(max_length=20)
    # username = models.CharField(max_length=20, unique=True)
    # password = models.CharField(max_length=20)
    role = models.CharField(max_length=10, choices=ROLES, default="member")
    age = models.IntegerField(null=True)
    locations = models.ManyToManyField(Location)

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ["username"]

    def __str__(self):
        return self.username
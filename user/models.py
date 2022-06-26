from datetime import date
from dateutil.relativedelta import relativedelta

from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models

# Create your models here.
from location.models import Location

MIN_AGE = 9


def AgeCheckValidator(value: date):
    difference = relativedelta(date.today(), value).years
    if difference < MIN_AGE:
        raise ValidationError(
            "%(value) is too small",
            params={"value", value}
        )


class User(AbstractUser):
    MEMBER = "member"
    MODERATOR = "moderator"
    ADMIN = "admin"

    ROLES = [(MEMBER, "Пользователь"), (MODERATOR, "Модератор"), (ADMIN, "Админ")]

    role = models.CharField(max_length=10, choices=ROLES, default="member")
    age = models.IntegerField(null=True)
    locations = models.ManyToManyField(Location)
    birth_date = models.DateField(null=True, validators=[AgeCheckValidator])
    email = models.EmailField(unique=True, null=True)

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ["username"]

    def __str__(self):
        return self.username
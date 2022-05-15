
from django.db import models

#
# class Ad(models.Model):
#     name = models.CharField(max_length=100)
#     author = models.CharField(max_length=100)
#     price = models.IntegerField(default=0)
#     description = models.CharField(max_length=1000)
#     address = models.CharField(max_length=120)
#     is_published = models.BooleanField(default=False)
#
#     class Meta:
#         verbose_name = "Объявление"
#         verbose_name_plural = "Объявления"
#
#     def __str__(self):
#         return self.name
#
#
# class Category(models.Model):
#     name = models.CharField(max_length=30)
#
#     class Meta:
#         verbose_name = "Категория"
#         verbose_name_plural = "Категории"
#
#     def __str__(self):
#         return self.name


# class Location(models.Model):
#     name = models.CharField(max_length=100)
#     lat = models.DecimalField(decimal_places=6, max_digits=10)
#     lng = models.DecimalField(decimal_places=6, max_digits=10)
#
#     class Meta:
#         verbose_name = "Локация"
#         verbose_name_plural = "Локации"
#
#     def __str__(self):
#         return self.name
#
#
# class User(models.Model):
#     ROLES = [("member", "Пользователь"), ("moderator", "Модератор"), ("admin", "Админ")]
#
#     first_name = models.CharField(max_length=20)
#     last_name = models.CharField(max_length=20)
#     username = models.CharField(max_length=20)
#     password = models.CharField(max_length=20)
#     role = models.CharField(max_length=10, choices=ROLES, default="member")
#     age = models.IntegerField()
#     location_id = models.ForeignKey(Location, on_delete=models.CASCADE)
#
#     class Meta:
#         verbose_name = "Пользователь"
#         verbose_name_plural = "Пользователи"
#
#     def __str__(self):
#         return self.username

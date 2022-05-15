from django.db import models

# Create your models here.

class Location(models.Model):
    name = models.CharField(max_length=100)
    lat = models.DecimalField(decimal_places=6, max_digits=10, default=0.0)
    lng = models.DecimalField(decimal_places=6, max_digits=10, default=0.0)

    class Meta:
        verbose_name = "Локация"
        verbose_name_plural = "Локации"

    def __str__(self):
        return self.name
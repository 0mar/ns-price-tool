from django.db import models


# Create your models here.

class Station(models.Model):
    code = models.CharField(max_length=10)
    latitude = models.FloatField()
    longitude = models.FloatField()
    short = models.CharField(max_length=50)
    medium = models.CharField(max_length=50)
    long = models.CharField(max_length=50)

    def __str__(self):
        return self.short

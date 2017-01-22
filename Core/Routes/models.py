from django.db import models


# Create your models here.
from Core.Account.models import User


class Route(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    campus_pk = models.IntegerField(default=0)
    car_pk = models.IntegerField(default=0)
    name = models.CharField(max_length=75)
    origin = models.CharField(max_length=75)
    sits = models.IntegerField(default=0)
    start_time = models.TimeField(auto_now=True)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return u"%s" % (self.name)


class RouteDay(models.Model):
    route = models.ForeignKey(
        Route,
        on_delete=models.CASCADE
    )
    day = models.CharField(max_length=75, default='')


class RouteMarker(models.Model):
    route = models.ForeignKey(
        Route,
        on_delete=models.CASCADE
    )
    position = models.IntegerField(default=0)
    latitude = models.CharField(max_length=150, default='')
    longitude = models.CharField(max_length=150, default='')

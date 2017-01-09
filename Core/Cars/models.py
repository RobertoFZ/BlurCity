from django.db import models

# Create your models here.
from Core.Account.models import User


class Car(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    model = models.CharField(max_length=30)
    brand = models.CharField(max_length=30)
    registration_tag = models.CharField(max_length=30)
    color = models.CharField(max_length=30)
    total_sits = models.IntegerField()

    def __str__(self):
        return self.model

    def __unicode__(self):
        return u"%s" % (self.model)

class CarDocument(models.Model):
    car = models.OneToOneField(
        Car,
        on_delete=models.CASCADE,
        primary_key=True
    )
    insurance_policy = models.ImageField(upload_to='static/uploads/documents/')
    circulation_card = models.ImageField(upload_to='static/uploads/documents/')
    licence = models.ImageField(upload_to='static/uploads/documents/')

    def __str__(self):
        return self.car.model

    def __unicode__(self):
        return u"%s" % (self.car.model)

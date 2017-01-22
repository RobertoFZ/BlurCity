#!/usr/bin/python
# -*- coding: latin-1 -*-

from django.db import models


# Create your models here.


class University(models.Model):
    name = models.CharField(max_length=75, unique=True)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return u"%s" % (self.name)


class Campus(models.Model):
    university = models.ForeignKey(
        University,
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=150, default="0")
    latitude = models.CharField(max_length=150, default='0')
    longitude = models.CharField(max_length=150, default='0')

    def __str__(self):
        return self.name

    def __unicode__(self):
        return u"%s" % (self.name)


class Major(models.Model):
    campus = models.OneToOneField(
        Campus,
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=150, default="0")

    def __str__(self):
        return self.name

    def __unicode__(self):
        return u"%s" % (self.name)

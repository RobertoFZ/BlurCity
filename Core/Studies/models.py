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


class Major(models.Model):
    university = models.OneToOneField(
        University,
        on_delete=models.CASCADE,
        primary_key=True
    )
    name = models.CharField(max_length=75)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return u"%s" % (self.name)

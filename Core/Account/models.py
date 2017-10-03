#!/usr/bin/python
# -*- coding: latin-1 -*-
import os

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.utils.text import slugify
from django.utils.translation import ugettext as _


# Create your models here.
from Core.Studies.models import University, Campus, Major


class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('El usuario deberia tener un nombre de usuario')

        user = self.model(
            email=email,
        )

        user.set_password = (password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password=password)
        user.is_admin = True
        user.save(using=self._db)
        return user


def image_path(self, filename):
    extension = os.path.splitext(filename)[1][1:]
    file_name = os.path.splitext(filename)[0]
    url = "users/%s/profile/%s.%s" % (self.id, slugify(str(file_name)), extension)
    return url

class User(AbstractBaseUser):

    USER_ADMIN_TYPE = (
        (0, _(u"Superusuario")),
        (1, _(u"Universidad")),
        (2, _(u"Facultad")),
        (3, _(u"Usuario"))
    )

    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    image_profile = models.ImageField(upload_to=image_path, null=True, blank=True, verbose_name="Imagen de perfil")
    #university = models.IntegerField(null=True, blank=True)
    university = models.ForeignKey(University, null=True, blank=True)
    #major = models.IntegerField(null=True, blank=True)
    major = models.ForeignKey(Major, null=True, blank=True)
    is_validated = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=True)
    user_admin_type = models.IntegerField(choices=USER_ADMIN_TYPE, default=3)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def get_full_name(self):
        '''
        Returns the first_name plus the last_name, with a space in between.
        '''
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        '''
        Returns the short name for the user.
        '''
        return self.first_name

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    def __str__(self):
        return self.email

    def __unicode__(self):
        return u"%s" % self.email

from django.db import models

# Create your models here.
from Core.Account.models import User


class Notification(models.Model):
    user = models.ForeignKey(
        User,
        on_delete= models.CASCADE
    )
    request_user = models.IntegerField()
    status = models.BooleanField()
    route_pk = models.IntegerField()
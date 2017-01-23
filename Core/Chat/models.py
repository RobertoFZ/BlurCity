from django.db import models

# Create your models here.
from Core.Account.models import User


class Room(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    user_chat_request = models.IntegerField()


class Message(models.Model):
    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE
    )
    message = models.CharField(max_length=500)
    user_pk = models.IntegerField()
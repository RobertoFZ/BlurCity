from django.contrib import admin

# Register your models here.
from Core.Notifications.models import Notification

admin.site.register(Notification)
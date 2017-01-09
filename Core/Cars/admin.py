from django.contrib import admin

# Register your models here.
from Core.Cars.models import CarDocument, Car

admin.site.register(Car)
admin.site.register(CarDocument)
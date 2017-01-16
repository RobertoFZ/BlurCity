from django.contrib import admin

# Register your models here.
from Core.Routes.models import Route, RouteDay, RouteMarker

admin.site.register(Route)
admin.site.register(RouteDay)
admin.site.register(RouteMarker)

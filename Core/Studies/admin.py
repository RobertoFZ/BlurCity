from django.contrib import admin

# Register your models here.
from Core.Studies.models import Major, University

admin.site.register(University)
admin.site.register(Major)

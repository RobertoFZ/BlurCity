from django.contrib import admin

# Register your models here.
from Core.Studies.models import Major, University, Campus

admin.site.register(University)
admin.site.register(Major)
admin.site.register(Campus)

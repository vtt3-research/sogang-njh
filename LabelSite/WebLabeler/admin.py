from django.contrib import admin

# Register your models here.
import models

admin.site.register(models.Media)
admin.site.register(models.ContentInformation)
admin.site.register(models.Shot)
from django.contrib import admin
from . import models


# Register your models here.


class ParentAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'username', 'email', 'locality', 'county')

class ChildAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name')

class DeviceAdmin(admin.ModelAdmin):
    list_display = ('id',)

class Danger_zoneAdmin(admin.ModelAdmin):
    list_display = ('id', 'coordinates')

class Approved_zoneAdmin(admin.ModelAdmin):
    list_display = ('id', 'coordinates')


admin.site.register(models.Parent, ParentAdmin)
admin.site.register(models.Child, ChildAdmin)
admin.site.register(models.Device, DeviceAdmin)
admin.site.register(models.Danger_zone, Danger_zoneAdmin)
admin.site.register(models.Approved_zone, Approved_zoneAdmin)

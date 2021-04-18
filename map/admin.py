from django.contrib import admin

from database.models import Notification
admin.register(Notification)(admin.ModelAdmin)
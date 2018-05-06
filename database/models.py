from django.db import models
from licenta.settings import SESSION_USER_ID_FIELD_NAME

# Create your models here.

class Parent(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=100)
    locality = models.CharField(max_length=20)
    county = models.CharField(max_length=20)
    phone = models.CharField(max_length=10)
    username = models.CharField(max_length=26, unique=True)
    password = models.CharField(max_length=30)

    @classmethod
    def authenticate(cls, username, password):
        try:
            return cls.objects.get(username=username, password=password)
        except Exception:
            return None

    def login(self, request):
        request.session[SESSION_USER_ID_FIELD_NAME] = self.id

    def logout(self, request):
        if request.session:
            del request.session


class Child(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)


class Parent_Child(models.Model):
    parent_id = models.ForeignKey(Parent, on_delete=models.CASCADE)
    child_id = models.ForeignKey(Child, on_delete=models.CASCADE)


class Device(models.Model):
    token = models.CharField(max_length=10)
    latitude = models.FloatField()
    longitude = models.FloatField()
    activated = models.BooleanField()


class Child_Device(models.Model):
    child_id = models.ForeignKey(Child, on_delete=models.CASCADE)
    device_id = models.ForeignKey(Device, on_delete=models.CASCADE)


class Danger_zone(models.Model):
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=300)
    coordinates = models.CharField(max_length=4096)


class Parent_Danger_zone(models.Model):
    parent_id = models.ForeignKey(Parent, on_delete=models.CASCADE)
    danger_zone_id = models.ForeignKey(Danger_zone, on_delete=models.CASCADE)


class Approved_zone(models.Model):
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=300)
    coordinates = models.CharField(max_length=4096)


class Parent_Approved_zone(models.Model):
    parent_id = models.ForeignKey(Parent, on_delete=models.CASCADE)
    approved_zone_id = models.ForeignKey(Approved_zone, on_delete=models.CASCADE)


class Notification(models.Model):
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=300)


class Parent_Noification(models.Model):
    parent_id = models.ForeignKey(Parent, on_delete=models.CASCADE)
    notification_id = models.ForeignKey(Notification, on_delete=models.CASCADE)

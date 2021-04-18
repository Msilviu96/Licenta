import datetime

from django.db import models

from MONAPP.settings import SESSION_USER_ID_FIELD_NAME


# Create your models here.

class Parent(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=100)
    locality = models.CharField(max_length=20)
    county = models.CharField(max_length=20)
    phone = models.CharField(max_length=10)
    birth_day = models.DateField(null=True)
    gender = models.CharField(max_length=1)
    username = models.CharField(max_length=26, unique=True)
    password = models.CharField(max_length=30)
    image = models.ImageField(upload_to='profile_image', blank=True)

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


class Danger_zone(models.Model):
    parent = models.ForeignKey(Parent, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=300)
    coordinates = models.CharField(max_length=4096)


class Child(models.Model):
    parent = models.ForeignKey(Parent, on_delete=models.CASCADE, null=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    birth_day = models.DateField(null=True)
    gender = models.CharField(max_length=1)
    image = models.ImageField(upload_to='profile_image', blank=True)


class Device(models.Model):
    child = models.ForeignKey(Child, on_delete=models.CASCADE, null=True)
    token = models.CharField(max_length=10)
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)
    activated = models.BooleanField()
    current_zone = models.ForeignKey(Danger_zone, on_delete=models.SET_DEFAULT, null=True, default=None)
    mockedLocation = models.BooleanField(default=False)


class Approved_zone(models.Model):
    parent = models.ForeignKey(Parent, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=300)
    coordinates = models.CharField(max_length=4096)


class Notification(models.Model):
    parent = models.ForeignKey(Parent, on_delete=models.CASCADE, null=True)
    device = models.ForeignKey(Device, on_delete=models.CASCADE, null=True)
    description = models.CharField(max_length=300)
    read = models.BooleanField(default=False)


class Message(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE, null=True)
    message = models.CharField(max_length=300)
    creation_time = models.DateTimeField(default=datetime.datetime.now())
    sent = models.BooleanField(default=False)
    read = models.BooleanField(default=False)


class Applications(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE, null=True)
    app_list = models.CharField(max_length=10000, null=True)

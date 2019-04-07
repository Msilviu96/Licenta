from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from django.forms.models import model_to_dict

from MONAPP.settings import SESSION_USER_ID_FIELD_NAME
from database import models
from database.models import Device, Child

from shapely.geometry import Point
from shapely.geometry.polygon import Polygon


class Token(APIView):
    def get(self, request, token):
        print(token)
        device_query_set = Device.objects.filter(token=token)
        if device_query_set:
            device = device_query_set[0]
            child = model_to_dict(Child.objects.get(pk=device.child_id))
            child['token'] = token
            device.activated = True
            device.save()
            return Response(child, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


class Coordinates(APIView):
    def post(self, request, token):
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')

        Device.objects.filter(token=token).update(
            latitude=latitude,
            longitude=longitude
        )

        device = models.Device.objects.get(token=token)
        parent = device.child.parent
        danger_zones = models.Danger_zone.objects.filter(parent=parent).select_related()
        point = Point(float(latitude), float(longitude))

        for danger_zone in danger_zones:
            coordinates = eval(danger_zone.coordinates)
            inverted = [(l[1], l[0]) for l in coordinates]
            polygon = Polygon(inverted)
            print(polygon.contains(point))

        return Response(status=status.HTTP_200_OK)

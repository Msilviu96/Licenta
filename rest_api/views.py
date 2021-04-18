import base64
import datetime
import json
import time

from django.http import JsonResponse, QueryDict
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from django.forms.models import model_to_dict

from MONAPP.settings import SESSION_USER_ID_FIELD_NAME, MEDIA_ROOT
from database import models
from database.models import Device, Child

from shapely.geometry import Point
from shapely.geometry.polygon import Polygon


class Token(APIView):
    def get(self, request, token):
        device_query_set = Device.objects.filter(token=token)
        if device_query_set:
            device = device_query_set[0]
            device.save()
            child = model_to_dict(Child.objects.get(pk=device.child_id))
            child['token'] = token
            with open(child['image'].path, 'rb') as img:
                encoded_string = base64.b64encode(img.read())
            child['image'] = encoded_string.decode('utf-8').replace("/", "\/")
            device.activated = True
            device.save()

            return Response(child, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


class Coordinates(APIView):
    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super(Coordinates, self).dispatch(*args, **kwargs)

    def update_coordinates(self, token, latitude, longitude):
        Device.objects.filter(token=token).update(
            latitude=latitude,
            longitude=longitude
        )

    def check_for_mocked_location(self, device, parent, isMocked):
        if not device.mockedLocation and isMocked == "1":
            self.notify_mocked_location(parent, device)
            device.mockedLocation = True
            device.save()

        if isMocked is "0":
            device.mockedLocation = False
            device.save()

    def get_danger_zones(self, parent):
        return models.Danger_zone.objects.filter(parent=parent).select_related()

    def check_child_position(self, point, device, parent):
        danger_zones = self.get_danger_zones(parent)

        for danger_zone in danger_zones:
            coordinates = eval(danger_zone.coordinates)
            inverted = [(l[1], l[0]) for l in coordinates]
            polygon = Polygon(inverted)
            if polygon.contains(point):
                if not device.current_zone:
                    device.current_zone = danger_zone
                    self.create_notification(parent, device, danger_zone)
                elif device.current_zone.pk != danger_zone.pk:
                    device.current_zone = danger_zone
                    self.create_notification(device, danger_zone)
            else:
                device.current_zone = None
        device.save()

    def post(self, request, token):
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        applications = eval(request.POST.get('applications'))
        isMocked = request.POST.get('isMocked')

        device = models.Device.objects.get(token=token)
        parent = device.child.parent
        point = Point(float(latitude), float(longitude))

        self.update_coordinates(token, latitude, longitude)
        self.check_for_mocked_location(device, parent, isMocked)
        self.check_child_position(point, device, parent)
        self.process_application_list(parent, device, applications)

        try:
            messages = models.Message.objects.filter(device=device, sent=False)
            stored_messages = list()

            for message in messages:
                    stored_messages.append({
                        'creation_time': message.creation_time.strftime("%d-%m-%Y %H:%M:%S"),
                        'text': message.message,
                        'id': message.id
                    })
                    message.sent = True
                    message.save()

            stored_apps = models.Applications.objects.filter(device=device)
            if stored_apps:
                stored_apps = eval(stored_apps.first().app_list.replace('\'', '"'))
            else:
                stored_apps = list()

            r
            esponse = {'action': 'completed',
                       'messages': stored_messages,
                       'applications': stored_apps
                       }
            return JsonResponse(response, status=200)
        except Exception as e:
            for message in messages:
                message.sent = False
                message.save()
            return JsonResponse({'action': 'failed'}, status=500)

    def create_notification(self, parent, device, model):
        child = device.child

        if isinstance(model, models.Danger_zone):
            description = "Entered the zone {}".format(model.title)
        else:
            description = "Installed new app: {}".format(model)

        models.Notification.objects.create(
            parent=parent,
            device=device,
            description=description,
            read=False
        )

    def notify_mocked_location(self, parent, device):
        models.Notification.objects.create(
            parent=parent,
            device=device,
            description="Location is mocked!",
            read=False
        )

    def process_application_list(self, parent, device, received_apps):
        received_apps = sorted(received_apps, key=lambda k: k['name'])
        database_info = models.Applications.objects.filter(device=device)

        to_store_apps = list()

        if not database_info:
            models.Applications.objects.create(
                device=device,
                app_list=str(received_apps),
            )
            return

        database_info = database_info.first()
        database_apps = eval(database_info.app_list)

        if len(database_info.app_list) == 2:
            database_info.app_list = str(received_apps)
            database_info.save()
            return

        flag_append = False

        for i in range(len(received_apps)):
            for j in range(len(database_apps)):
                flag_append = True
                if received_apps[i]['name'] == database_apps[j]['name']:
                    to_store_apps.append({
                        "name": database_apps[j]['name'],
                        "blocked": database_apps[j]['blocked']
                    })
                    flag_append = False
                    break
                elif received_apps[i]['name'][0] < database_apps[j]['name'][0]:
                    to_store_apps.append({
                        "name": received_apps[i]['name'],
                        "blocked": received_apps[i]['blocked']
                    })
                    self.create_notification(parent, device, received_apps[i]['name'])
                    flag_append = False
                    break
            if flag_append:
                to_store_apps.append({
                    "name": received_apps[i]['name'],
                    "blocked": received_apps[i]['blocked']
                })
                self.create_notification(parent, device, received_apps[i]['name'])

        database_info.app_list = str(to_store_apps)
        database_info.save()


class Message(APIView):
    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super(Message, self).dispatch(*args, **kwargs)

    def get(self, request):
        response = list()
        try:
            device = models.Device.objects.filter(token=request.GET.get('token')).first()
            print(device.token)
            messages = models.Message.objects.filter(device=device)

            for message in messages:
                response.append({
                    'message': message.message,
                    'creation_time': message.creation_time,
                    'read': message.read,
                    'sent': message.sent
                })
        except Exception as e:
            print(e)

        return JsonResponse({'messages': response})

    def post(self, request):
        try:
            device = models.Device.objects.filter(token=request.POST.get('token')).first()
            models.Message.objects.create(
                device=device,
                message=request.POST.get('message'),
                creation_time=datetime.datetime.now(),
                sent=False,
            )
        except Exception as e:
            print(e)
            return JsonResponse({'action': 'failed'}, status=500)
        else:
            return JsonResponse({'action': 'completed'}, status=200)

    def put(self, request):
        put = QueryDict(request.body)
        messages = json.loads(put.get('messages'))
        token = put.get('token')
        try:
            device = models.Device.objects.filter(token=token).first()
            for message in messages:
                m = models.Message.objects.filter(id=message['id']).first()
                m.read = True
                m.save()
        except Exception as e:
            print(e)
            return JsonResponse({'action': 'failed'}, status=500)

        return JsonResponse({'action': 'completed'})

class Application(APIView):
    def post(self, request):
        token = request.POST.get('token')
        received_apps = eval(request.POST.get('apps'))
        device = models.Device.objects.filter(token=token).first()
        database_info = models.Applications.objects.filter(device=device).first()
        database_apps = eval(database_info.app_list)

        to_store_apps = []
        flag_append = False

        for i in range(len(received_apps)):
            for j in range(len(database_apps)):
                flag_append = True
                if received_apps[i]['name'] == database_apps[j]['name']:
                    to_store_apps.append({
                        "name": received_apps[j]['name'],
                        "blocked": received_apps[j]['blocked']
                    })
                    flag_append = False
                    break
                elif received_apps[i]['name'][0] > database_apps[j]['name'][0]:
                    to_store_apps.append({
                        "name": received_apps[i]['name'],
                        "blocked": received_apps[i]['blocked']
                    })
                    flag_append = False
                    break
            if flag_append:
                to_store_apps.append({
                    "name": received_apps[i]['name'],
                    "blocked": received_apps[i]['blocked']
                })

        database_info.app_list = str(to_store_apps)
        database_info.save()

        return JsonResponse({'action': 'completed'}, status=200)

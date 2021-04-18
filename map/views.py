from django.shortcuts import render, redirect
from django.views.generic import View
from authentication.authentification import logged_in_only
from django.http import JsonResponse, QueryDict
from django.views.decorators.csrf import csrf_exempt

from database import models
from MONAPP.settings import SESSION_USER_ID_FIELD_NAME

import json
from MONAPP.pusher import Pusher


class Map(View):
    html = 'map/map.html'

    def get(self, request):
        token = request.GET.get('token')
        if token:
            device = models.Device.objects.get(token=token)
            return JsonResponse({
                'latitude': device.latitude,
                'longitude': device.longitude,
                'name': device.child.first_name,
            })

        kids = models.Child.objects.filter(parent=request.session.get(SESSION_USER_ID_FIELD_NAME)).select_related()

        if len(kids) == 0:
            request.session['error'] = 'You need to have at least one child registered!'
            return redirect('child:child')

        activated_devices = self.get_activated_devices(kids)
        if len(activated_devices) == 0:
            return render(request, self.html, context={
                'error': 'You need to activate at least one device'
            })

        return render(request, self.html, context={
            'devices': activated_devices,
            'token': activated_devices[0].token
        })

    @staticmethod
    def get_activated_devices(kids):
        activated_devices = list()
        for kid in kids:
            device = models.Device.objects.get(child=kid)
            if device.activated:
                activated_devices.append(device)

        return activated_devices


class DangerZone(View):
    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super(DangerZone, self).dispatch(*args, **kwargs)

    @logged_in_only
    def post(self, request):
        coordinates = str(json.loads(request.POST.get('data'))['geometry']['coordinates'][0])
        title = request.POST.get('title')
        parent = models.Parent.objects.filter(pk=request.session.get(SESSION_USER_ID_FIELD_NAME)).first()

        try:
            models.Danger_zone.objects.create(
                parent=parent,
                title=title,
                description='',
                coordinates=coordinates
            )
            return JsonResponse({'error': ''})
        except Exception as e:
            return JsonResponse({'error': e})

    @logged_in_only
    def get(self, request):
        parent = models.Parent.objects.filter(pk=request.session.get(SESSION_USER_ID_FIELD_NAME)).first()
        danger_zones = models.Danger_zone.objects.filter(parent=parent).select_related()
        danger_zones_coordinates = list()

        for danger_zone in danger_zones:
            danger_zones_coordinates.append([eval(danger_zone.coordinates), danger_zone.title])

        return JsonResponse({
            'data': danger_zones_coordinates
        })

    @logged_in_only
    def delete(self, request):
        delete = QueryDict(request.body)
        coordinates = str(json.loads(delete.get('data'))['geometry']['coordinates'][0])

        danger_zone = models.Danger_zone.objects.filter(coordinates=coordinates).first()
        danger_zone.delete()

        return JsonResponse({
            'error': ''
        })

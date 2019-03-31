from django.shortcuts import render, redirect
from django.views.generic import View
from authentication.authentification import logged_in_only
from django.http import JsonResponse


from database import models
from MONAPP.settings import SESSION_USER_ID_FIELD_NAME
from MONAPP.pusher import Pusher


class Map(View):
    html = 'map/map.html'

    @logged_in_only
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


    def post(self, request):

        return render(request, self.html, context={})

    @staticmethod
    def get_activated_devices(kids):
        activated_devices = list()
        for kid in kids:
            device = models.Device.objects.get(child=kid)
            if device.activated:
                activated_devices.append(device)

        return activated_devices

from django.http import JsonResponse, QueryDict
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from authentication.authentification import logged_in_only

from database import models
from MONAPP.settings import SESSION_USER_ID_FIELD_NAME, MEDIA_ROOT, MEDIA_URL

import string
from random import choice
from datetime import datetime


class Child(View):
    html = 'child/child.html'

    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super(Child, self).dispatch(*args, **kwargs)

    @logged_in_only
    def get(self, request):
        logged_user = request.session.get(SESSION_USER_ID_FIELD_NAME)
        notifications = self.get_notifications(logged_user)

        return render(request, "child/child.html", context={
            'notifications': notifications,
            'user': logged_user
        })

    @staticmethod
    def get_notifications(logged_user):
        return list(models.Notification.objects.filter(parent=logged_user, read=False))

    @logged_in_only
    def post(self, request):
        token = self.generate_child_token()
        parent = models.Parent.objects.get(pk=request.session.get(SESSION_USER_ID_FIELD_NAME))

        try:
            child = models.Child.objects.create(
                parent=parent,
                first_name=request.POST.get('fname'),
                last_name=request.POST.get('lname'),
                birth_day=datetime.strptime(request.POST.get('bday'), '%d-%m-%Y'),
                gender=request.POST.get('gender'),
                image='profile_image/blank_profile_image.png'
            )

            if child:
                models.Device.objects.create(
                    child=child,
                    token=token,
                    latitude=0,
                    longitude=0,
                    activated=False,
                )
        except Exception as e:
            print(e)
            return JsonResponse({'error': e})

        return JsonResponse({'token': token})

    @staticmethod
    def generate_child_token():
        alphabet = string.ascii_letters + string.digits

        token = ''.join([choice(alphabet) for _ in range(7)])
        while Child.is_already_generated(token):
            token = ''.join([choice(alphabet) for _ in range(7)])

        return token

    @staticmethod
    def is_already_generated(token):
        device = models.Device.objects.filter(token=token)
        if device:
            return True
        else:
            return False

    @staticmethod
    def decode(target, to_compare='', to_decode=None):
        if target == to_compare:
            return to_decode
        else:
            return target

    def put(self, request):
        put = QueryDict(request.body)
        first_name = self.decode(put.get('fname'))
        last_name = self.decode(put.get('lname'))
        token = self.decode(put.get('token'))

        device = models.Device.objects.filter(token=token).first()
        child: models.Child = device.child

        if not first_name:
            first_name = child.first_name

        if not last_name:
            last_name = child.last_name

        child.first_name = first_name
        child.last_name = last_name

        child.save()

        return JsonResponse({'action': 'completed'})


def check_token(request):
    token = request.GET.get('token')
    device = models.Device.objects.filter(token=token).first()
    if device:
        return JsonResponse({'activated': device.activated})

    return JsonResponse({'activated': False})

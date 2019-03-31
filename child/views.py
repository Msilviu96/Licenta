from django.shortcuts import render, redirect
from django.views.generic import View
from authentication.authentification import logged_in_only
from django.http import HttpResponse

from database import models
from MONAPP.settings import SESSION_USER_ID_FIELD_NAME
import database

import string
from random import choice
from datetime import datetime


class Child(View):
    html = 'child/child.html'

    @logged_in_only
    def get(self, request):
        msg = request.session.pop('msg', None)
        context = {}
        if msg:
            context['msg'] = msg
        return render(request, self.html, context=context)


@logged_in_only
def post(self, request):
    token = self.generate_child_token()
    parent = models.Parent.objects.get(pk=request.session.get(SESSION_USER_ID_FIELD_NAME))

    try:
        child = models.Child.objects.create(
            parent=parent,
            first_name=request.POST.get('fname'),
            last_name=request.POST.get('lname'),
            birth_day=datetime.strptime(request.POST.get('bday'), '%Y-%m-%d'),
            gender=request.POST.get('gender'),
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
        return render(request, self.html, {'error': e})

    return render(request, self.html, {'error': token})


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

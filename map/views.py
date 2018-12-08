from django.shortcuts import render, redirect
from django.views.generic import View
from authentication.authentification import logged_in_only
from django.http import HttpResponse

from database import models
from licenta.settings import SESSION_USER_ID_FIELD_NAME


class Map(View):
    html = 'map/map.html'

    @logged_in_only
    def get(self, request):
        return render(request, self.html)

    def post(self, request):
        pass

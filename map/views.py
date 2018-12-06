from django.shortcuts import render, redirect
from django.views.generic import View
from django.http import HttpResponse

from database import models
from licenta.settings import SESSION_USER_ID_FIELD_NAME


class Map(View):
    html = 'map/map.html'

    def get(self, request):
        return render(request, self.html)

    def post(self, request):
        pass

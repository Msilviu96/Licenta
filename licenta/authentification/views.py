from django.shortcuts import render, redirect
from django.views.generic import View
from .authentification import logged_in_only
from django.http import HttpResponse, HttpResponseRedirect


from database import models
from licenta.settings import SESSION_USER_ID_FIELD_NAME

# Create your views here.


class Login(View):
    def get(self, request):
        if request.session.get(SESSION_USER_ID_FIELD_NAME):
            del request.session[SESSION_USER_ID_FIELD_NAME]
        return render(request, 'authentication/login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        parent = models.Parent.authenticate(username, password)
        if parent:
            parent.login(request)
            return redirect('authentication:profile')
        else:
            return render(request, 'authentication/login.html', context={
                "error": "Invalid username / password."
            })

def register(request):
    return HttpResponse("<h1> Register </h1>")

class Profile(View):

    @logged_in_only
    def get(self, reguest):
        return HttpResponse('<h1> Profile </h1>')


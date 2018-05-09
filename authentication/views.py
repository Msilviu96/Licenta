from django.shortcuts import render, redirect
from django.views.generic import View
from .authentification import logged_in_only
from django.http import HttpResponse, HttpResponseRedirect

from database import models
from licenta.settings import SESSION_USER_ID_FIELD_NAME


# Create your views here.


class Login(View):
    html = 'authentication/login.html'

    def get(self, request):
        if request.session.get(SESSION_USER_ID_FIELD_NAME):
            del request.session[SESSION_USER_ID_FIELD_NAME]
        return render(request, self.html)

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        parent = models.Parent.authenticate(username, password)
        if parent:
            parent.login(request)
            return redirect('authentication:profile')
        else:
            return render(request, self.html, context={
                "error": "Invalid username / password."
            })


class Register(View):
    html = 'authentication/register.html'

    def get(self, request):
        if request.session.get(SESSION_USER_ID_FIELD_NAME):
            del request.session[SESSION_USER_ID_FIELD_NAME]
        return render(request, self.html)

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirmation = request.POST.get('confirmation')

        if password != confirmation:
            return render(request, self.html, {'error': 'Confirmation password is different'})

        try:
            models.Parent.objects.create(
                first_name=request.POST.get('fname'),
                last_name=request.POST.get('lname'),
                email=request.POST.get('email'),
                locality=request.POST.get('locality'),
                county=request.POST.get('county'),
                phone=request.POST.get('phone'),
                username=request.POST.get('username'),
                password=request.POST.get('password'),
            )
        except Exception as e:
            return render(request, self.html, {'error': e})
        else:
            parent = models.Parent.authenticate(username, password)
            if parent:
                parent.login(request)
                return redirect('authentication:profile')
            else:
                return render(request, self.html, context={
                    "error": "Something went wrong!"
                })


class Profile(View):

    @logged_in_only
    def get(self, reguest):
        return HttpResponse('<h1> Profile </h1>')

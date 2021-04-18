import json

from django.http import QueryDict, JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View

from database import models
from MONAPP.settings import SESSION_USER_ID_FIELD_NAME

from datetime import datetime


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
                # locality=request.POST.get('locality'),
                # county=request.POST.get('county'),
                phone=request.POST.get('phone'),
                birth_day=datetime.strptime(request.POST.get('bday'), '%d-%m-%Y'),
                # gender=request.POST.get('gender'),
                username=request.POST.get('username'),
                password=request.POST.get('password'),
                image='profile_image/blank_profile_image.png'
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
    @staticmethod
    def decode(device):
        if device.activated:
            return "Activated"
        return "Not Activated"

    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super(Profile, self).dispatch(*args, **kwargs)

    def get(self, request):
        logged_user = request.session.get(SESSION_USER_ID_FIELD_NAME)
        if logged_user:
            return self.profile(request, logged_user)
        else:
            return self.home(request)

    @classmethod
    def profile(cls, request, logged_user):
        notifications = cls.get_notifications(logged_user)
        parent = models.Parent.objects.filter(pk=logged_user).first()
        kids = models.Child.objects.filter(parent=parent)
        grouped = []
        for child in kids:
            device = models.Device.objects.filter(child=child).first()
            apps = models.Applications.objects.filter(device=device)
            if apps:
                # apps = eval(apps.first().app_list)
                apps = eval(apps.first().app_list)
            else:
                apps = [None]
            grouped.append([child, device, cls.decode(device), apps])

        return render(request, "authentication/profile.html", context={
            'notifications': notifications,
            'user': parent,
            'grouped': grouped,
        })

    @staticmethod
    def get_notifications(logged_user):
        return list(models.Notification.objects.filter(parent=logged_user, read=False))

    def post(self, request):
        pass

    def put(self, request):
        put = QueryDict(request.body)

        pk = put.get('pk')

        notification = models.Notification.objects.get(pk=pk)
        notification.read = True
        notification.save()

        return JsonResponse({
            'error': ''
        })

    @classmethod
    def home(cls, request):
        return render(request, "authentication/home.html")

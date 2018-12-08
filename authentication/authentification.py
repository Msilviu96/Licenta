from django.shortcuts import redirect

from licenta.settings import SESSION_USER_ID_FIELD_NAME

from django.contrib.sessions import models
from django.urls import reverse
from django.http import HttpResponseRedirect

from database import models


class Authenticator(object):

    def __init__(self):
        self.session = models.Session()

    def authenticate(self, request, username, password):
        parent = models.Parent.objects.get(username=username)
        return parent.first_name

    def get_user(self, user_id):
        parent = models.Parent.get(id=user_id)
        return parent


def logged_in_only(func):
    def wrap(self, request, *args, **kwargs):
        if request.session.get(SESSION_USER_ID_FIELD_NAME):
            return func(self, request, *args, **kwargs)
        return redirect('authentication:login')

    return wrap

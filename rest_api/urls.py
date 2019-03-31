from django.conf.urls import url
from . import views

app_name = "rest_api"

urlpatterns = [
    url(r'^token/(?P<token>[0-9A-Za-z]{7})$', views.Token.as_view(), name='token'),
    url(r'child_coordinates/(?P<token>[0-9A-Za-z]{7})$', views.Coordinates.as_view(), name='coordinates'),
]

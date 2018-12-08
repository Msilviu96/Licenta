from django.conf.urls import url
from . import views

app_name = "child"

urlpatterns = [
    url(r'^$', views.Child.as_view(), name='child')
]

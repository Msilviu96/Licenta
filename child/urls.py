from django.conf.urls import url
from . import views

app_name = "child"

urlpatterns = [
    url(r'^$', views.Child.as_view(), name='child'),
    url(r'checkToken/', views.check_token, name='check_token'),
]

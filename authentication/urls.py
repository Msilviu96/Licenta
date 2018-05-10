from django.conf.urls import url
from . import views

app_name="authentication"

urlpatterns = [
    url(r'^$', views.Profile.as_view(), name='profile'),
    url(r'^login/$', views.Login.as_view(), name='login'),
    url(r'^register/$', views.Register.as_view(), name='register')
]
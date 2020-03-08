from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
    path('/home', views.Home, name='chat'),
    path('/post', views.Post, name='post'),
    path('/messages', views.Messages, name='messages'),
]

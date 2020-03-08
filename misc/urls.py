from django.contrib import admin
from django.urls import path,include
from django.conf.urls import url
from .views import *
from account.views import (
    logout_view,
    login_view,
)

urlpatterns = [
    path('',home2, name='home2'),
    path('logout/', logout_view, name="logout"),
    path('login/', login_view, name="login"),
    path('diary',diary_all2,name="diary_all2"),
    path('diary/<int:product_id>',detail2,name='detail2'),
    path('diary/<int:pk>/comment',comment,name="add_comment_to_post"),
    path('task',Assign,name="assign"),
    path('display',display,name="display"),
]

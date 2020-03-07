from django.contrib import admin
from django.urls import path
from .views import *
from account.views import (
    logout_view,
    login_view,
)


urlpatterns = [
    path('',home),
    path('diary/<int:product_id>/comment',add_comment_to_post,name="add_comment_to_post"),
]

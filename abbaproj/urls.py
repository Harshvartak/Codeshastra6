"""abbaproj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf.urls import url
from misc.views import *
import misc.urls
from account.views import (
    logout_view,
    login_view,
)
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',home, name='home'),
    path('logout/', logout_view, name="logout"),
    path('login/', login_view, name="login"),
    path('create/',create, name="create"),
    path('diary',diary_all,name="diary_all"),
    path('diary/<int:product_id>',detail,name='detail'),
    path('therapist/',include('misc.urls')),
    path('score/',score,name='score'),
    path('quiz/',quiz,name='quiz'),
    path('display',display2,name="display2"),
    path('display/<int:pk>',done2,name="edit"),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

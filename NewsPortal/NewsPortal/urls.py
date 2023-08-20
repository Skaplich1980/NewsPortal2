"""
URL configuration for NewsPortal project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, include

from . import views

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    #path('pages/', include('django.contrib.flatpages.urls')),
    # Делаем так, чтобы все адреса из нашего приложения (news/urls.py)
    # подключались к главному приложению с префиксом news/.
    path('news/', include('news.urls'), name='news'),
    path('about/', views.about, name='about'),
    path('contacts/', views.contacts, name='contact'),
    path('', views.index, name='index'),
]

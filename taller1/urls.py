"""taller1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from crawling import views as crawling_views
from rss import views as rss_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^rss/query', rss_views.query, name = 'query'),
    url(r'^rss/', rss_views.homerss, name = 'homerss'),
    url(r'^crawling/', crawling_views.homecrawling, name = 'homecrawling'),
   
]

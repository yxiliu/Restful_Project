"""Restful_Project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
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
from luffy import views as vluffy
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/', vluffy.Login().as_view()),
    url(r'^courses/$', vluffy.CoursesView.as_view()),
    url(r'^courses/(?P<pk>\d+)\.(?P<format>[a-z0-9]+)$', vluffy.CoursesView.as_view()),
    url(r'^news/$', vluffy.News().as_view()),
    url(r'^news/detail/(?P<nid>\d+)/$', vluffy.NewsDetail().as_view()),
]

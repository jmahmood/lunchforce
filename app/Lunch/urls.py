"""Lunch URL Configuration

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
from django.conf.urls import url, include
from django.contrib import admin
import django.contrib.auth.views
from django.http import HttpResponse
import os
import LunchCloud.views
from LunchCloud.forms import EmailAuthenticationForm
import rest_framework.authtoken.views

urlpatterns = [
    url(r'^$', LunchCloud.views.enrollment),
    url(r'^api/attend/$', LunchCloud.views.Attend.as_view()),
    url(r'^api/search/$', LunchCloud.views.Search.as_view()),
    url(r'^api/locations/$', LunchCloud.views.Locations.as_view()),
    url(r'^api/food-options/$', LunchCloud.views.FoodOptions.as_view()),
    url(r'^api/my-availability/$', LunchCloud.views.MyAvailability.as_view()),
    url(r'^api/update-availability/$', LunchCloud.views.CreateAvailability.as_view()),
    url(r'^api/public-appointments/$', LunchCloud.views.PublicLunchEvents.as_view()),
    url(r'^api/invitedto-appointments/$', LunchCloud.views.InvitedToEvents.as_view()),
    url(r'^api/my-appointments/$', LunchCloud.views.MyLunchAppointments.as_view()),
    url(r'^api/update-profile/$', LunchCloud.views.ProfileUpdate.as_view()),
    url(r'^api/my-profile/$', LunchCloud.views.MyProfileDetails.as_view()),
    url(r'^enroll/$', LunchCloud.views.enrollment),
    url(r'^login/$', LunchCloud.views.RedirectLoginView.as_view()),
    url(r'^admin/', admin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls')),
    url(r'^api-token-auth/', rest_framework.authtoken.views.obtain_auth_token)
]

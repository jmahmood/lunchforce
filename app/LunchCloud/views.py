# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
import json
import logging

from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import RedirectView
from rest_framework.views import APIView
import rest_framework.response
import LunchCloud.forms
from LunchCloud import serializers
from LunchCloud.models import Profile, InvitationCode, LunchEvents, Availability
from LunchCloud.serializers import ProfileSerializer, AppointmentSerializer


@login_required
def index(request: HttpRequest) -> HttpResponse:
    # This is a simple basic view which is powered by Angular.JS
    # It just displays your upcoming
    pass


def create_account(form_data: dict) -> (InvitationCode, Profile):
    ic = InvitationCode.objects.get(code=form_data.get('invitation_code'))

    prf: Profile = Profile(
        email=form_data.get('email'),
        blacklist=form_data.get('foods'),
        invited_by=ic.invited_by
    )
    return ic, prf


def enrollment(request: HttpRequest) -> HttpResponse:
    """
    User creates account and enrolls for system.

    :param request:
    :return:
    """
    frm: LunchCloud.forms.RegistrationForm

    if request.method == 'POST':
        frm = LunchCloud.forms.RegistrationForm(request.POST)

    if request.method == 'GET':
        frm = LunchCloud.forms.RegistrationForm({"invited_by": request.GET.get('invited_by', None)})

    if frm.is_valid():
        ic, prf = create_account(frm.cleaned_data)
        ic.used = True
        ic.save()
        prf.save()

        return redirect('my-dashboard', enrollment=True, profile=prf.pk)

    return render(
        request, 'enrollment.html', {'frm': frm}
    )

    pass


class RedirectLoginView(RedirectView):
    permanent = True
    url = '/account/login/'


class PublicLunchEvents(APIView):
    def get(self, request: HttpRequest, format=None):
        try:
            my_profile = self.request.user.profile
        except AttributeError:
            return rest_framework.response.Response(serializers.AppointmentAPISerializer({
                'success': False,
                'message': 'You are not logged in.',
                'appointments': None
            }).data)

        appointments = LunchEvents.objects.filter(
            is_private=False).filter(
            status='Proposed').filter(
            event_date__gt=datetime.date.today())

        serializer = serializers.AppointmentAPISerializer({
            'success': True,
            'message': None,
            'appointments': appointments
        })
        return rest_framework.response.Response(serializer.data)


class MyLunchEvents(APIView):
    def get(self, request: HttpRequest, format=None):
        try:
            my_profile = self.request.user.profile
        except AttributeError:
            return rest_framework.response.Response(serializers.AppointmentAPISerializer({
                'success': False,
                'message': 'You are not logged in.',
                'appointments': None
            }).data)

        appointments = my_profile.invited_to.all()

        serializer = serializers.AppointmentAPISerializer({
            'success': True,
            'message': None,
            'appointments': appointments
        })
        return rest_framework.response.Response(serializer.data)


class MyProfileDetails(APIView):
    def get(self, request: HttpRequest, format=None):
        try:
            my_profile = self.request.user.profile

        except AttributeError:
            return rest_framework.response.Response(serializers.ProfileAPISerializer({
                'success': False,
                'message': 'You are not logged in.',
                'updated': False,
                'profile': None
            }).data)

        serializer = serializers.ProfileAPISerializer({
            'success': True,
            'message': None,
            'updated': False,
            'profile': my_profile
        })

        return rest_framework.response.Response(serializer.data)


class MyAvailability(APIView):
    def get(self, request: HttpRequest, format=None):
        try:
            my_profile: Profile = self.request.user.profile

        except AttributeError:
            return rest_framework.response.Response(serializers.AvailabilityAPISerializer({
                'success': False,
                'message': 'You are not logged in.',
                'updated': False,
                'availability': None
            }).data)

        my_availability = my_profile.availability_set.filter(frm__gte=datetime.datetime.today())

        serializer = serializers.AvailabilityAPISerializer({
            'success': True,
            'message': None,
            'updated': False,
            'availability': my_availability
        })

        return rest_framework.response.Response(serializer.data)


class CreateAvailability(APIView):
    def post(self, request: HttpRequest, fmt=None):
        try:
            my_profile: Profile = self.request.user.profile

        except AttributeError:
            return rest_framework.response.Response(serializers.AvailabilityAPISerializer({
                'success': False,
                'message': 'You are not logged in.',
                'updated': False,
                'availability': None
            }).data)

        available_dates = json.loads(request.body)
        month = available_dates.get('month')
        dates = available_dates.get('date')

        # delete all dates in month and recreate
        existing_availability = my_profile.availability_set.filter(frm__month=month)
        existing_availability.delete()
        # delete them all

        all_availabilities: [Availability] = []

        for date in dates:
            logging.warning(date)
            y, m, d = date.split('-')
            logging.warning(date.split('-'))
            all_availabilities.append(Availability(
                frm=datetime.datetime(year=int(y), month=int(m), day=int(d), hour=9, minute=0, second=0),
                until=datetime.datetime(year=int(y), month=int(m), day=int(d), hour=18, minute=0, second=0),
                profile=my_profile
            ))

        Availability.objects.bulk_create(all_availabilities)
        serializer = serializers.AvailabilityAPISerializer({
            'success': True,
            'message': None,
            'updated': False,
            'availability': all_availabilities
        })

        return rest_framework.response.Response(serializer.data)


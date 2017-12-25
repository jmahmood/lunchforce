# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
import json
import logging

import rest_framework.response
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import RedirectView
from rest_framework.views import APIView

import LunchCloud.forms
from LunchCloud import serializers
from LunchCloud.helpers import date_from_string
from LunchCloud.models import Profile, IntroductionCode, LunchAppointment, Availability, FoodOption, Location


@login_required
def index(request: HttpRequest) -> HttpResponse:
    # This is a simple basic view which is powered by Angular.JS
    # It just displays your upcoming
    pass


def create_account(form_data: dict) -> (IntroductionCode, Profile):
    ic = IntroductionCode.objects.get(code=form_data.get('invitation_code'))

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


class InvitedToEvents(APIView):
    def get(self, request: HttpRequest, frmt=None):
        try:
            my_profile = self.request.user.profile
        except AttributeError:
            return rest_framework.response.Response(serializers.AppointmentAPISerializer({
                'success': False,
                'message': 'You are not logged in.',
                'appointments': None
            }).data)

        # This are, by nature, events that you are not invited to, but are public.
        appointments = LunchAppointment.objects.filter(
            status='proposed').filter(
            invitees__external_id__contains=my_profile.external_id).exclude(
            attendees__external_id__contains=my_profile.external_id)

        serializer = serializers.AppointmentAPISerializer({
            'success': True,
            'message': None,
            'appointments': appointments
        })
        return rest_framework.response.Response(serializer.data)


class PublicLunchEvents(APIView):
    def get(self, request: HttpRequest, frmt=None):
        try:
            my_profile = self.request.user.profile
        except AttributeError:
            return rest_framework.response.Response(serializers.AppointmentAPISerializer({
                'success': False,
                'message': 'You are not logged in.',
                'appointments': None
            }).data)

        # This are, by nature, events that you are not invited to, but are public.
        appointments = LunchAppointment.objects.filter(
            is_private=False).filter(
            event_date__gt=datetime.date.today()).exclude(
            invitees__external_id__contains=my_profile.external_id)

        serializer = serializers.AppointmentAPISerializer({
            'success': True,
            'message': None,
            'appointments': appointments
        })
        return rest_framework.response.Response(serializer.data)


class MyLunchAppointments(APIView):
    def get(self, request: HttpRequest, frmt=None):
        try:
            my_profile = self.request.user.profile
        except AttributeError:
            return rest_framework.response.Response(serializers.AppointmentAPISerializer({
                'success': False,
                'message': 'You are not logged in.',
                'appointments': None
            }).data)

        appointments = my_profile.confirmed.filter(event_date__gt=datetime.date.today())

        serializer = serializers.AppointmentAPISerializer({
            'success': True,
            'message': None,
            'appointments': appointments
        })
        return rest_framework.response.Response(serializer.data)


class ProfileUpdate(APIView):
    def post(self, request: HttpRequest, frmt=None) -> HttpResponse:
        try:
            my_profile: Profile = self.request.user.profile
        except AttributeError:
            return rest_framework.response.Response(serializers.ProfileAPISerializer({
                'success': False,
                'message': 'You are not logged in.',
                'updated': False,
                'profile': None
            }).data)

        post_data = json.loads(request.body)
        logging.debug(post_data)
        profile_details = post_data.get('profile')
        location_ids = [l.get('id') for l in profile_details.get('locations')]
        food_ids = [fo.get('id') for fo in profile_details.get('whitelist')]
        related_locations = Location.objects.filter(external_id__in=location_ids)
        related_foodoptions = FoodOption.objects.filter(external_id__in=food_ids)
        my_profile.locations = related_locations
        my_profile.whitelist = related_foodoptions
        my_profile.save()

        serializer = serializers.ProfileAPISerializer({
            'success': True,
            'message': None,
            'updated': False,
            'profile': my_profile
        })

        return rest_framework.response.Response(serializer.data)


class MyProfileDetails(APIView):
    def get(self, request: HttpRequest, frmt=None):
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
    def get(self, request: HttpRequest, frmt=None):
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
            dt = date_from_string(date)
            starting_time = datetime.time(hour=9, minute=0, second=0)
            ending_time = datetime.time(hour=18, minute=0, second=0)

            all_availabilities.append(Availability(
                frm=datetime.datetime.combine(dt, starting_time),
                until=datetime.datetime.combine(dt, ending_time),
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


class FoodOptions(APIView):
    def get(self, request: HttpRequest, fmt=None):
        food_options = FoodOption.objects.filter(enabled=True)

        serializer = serializers.FoodOptionAPISerializer({
            'success': True,
            'message': None,
            'food_options': food_options
        })

        return rest_framework.response.Response(serializer.data)


class Locations(APIView):
    def get(self, request: HttpRequest, fmt=None):
        locations = Location.objects.filter(enabled=True)

        serializer = serializers.LocationAPISerializer({
            'success': True,
            'message': None,
            'locations': locations
        })

        return rest_framework.response.Response(serializer.data)


class Search(APIView):
    def verbose_logging(self, my_profile: Profile, post_data):
        return """
Search request received

Requested by: {0}
Date Requested: {1}
Locations Requested: {2}
        """.format(
            my_profile.user.username,
            post_data.get('date'),
            post_data.get('location')
        )

    def verbose_appointment_logging(self, appointments: [LunchAppointment]):
        ret = []
        template = "{0} ({1}) - @ [{2} / {3} ({4})]"
        for app in appointments:
            ret.append(template.format(app.title, app.event_date, app.location, app.general_area.name,
                                       app.general_area.external_id))
        return '\n'.join(ret)

    def post(self, request: HttpRequest, fmt=None):

        try:
            my_profile: Profile = self.request.user.profile
        except AttributeError:
            return rest_framework.response.Response(serializers.SearchAPISerializer({
                'success': False,
                'message': 'You are not logged in.',
                'everyone': None,
                'youonly': None
            }).data)

        post_data = json.loads(request.body)
        logging.warning(self.verbose_logging(my_profile, post_data))

        location_ids = [loc.get('id') for loc in post_data.get('location')]
        dt = date_from_string(post_data.get('date'))

        appointments = LunchAppointment.objects.filter(
            general_area__external_id__in=location_ids).filter(
            event_date=dt)
        logging.debug("These were found:")
        logging.debug(self.verbose_appointment_logging(appointments))
        logging.debug("These are all available for the same date: {0}".format(dt))
        logging.debug(self.verbose_appointment_logging(LunchAppointment.objects.filter(event_date=dt)))
        logging.debug("These are all available for the same location: ({0})".format(location_ids))
        logging.debug(self.verbose_appointment_logging(LunchAppointment.objects.filter(
            eneral_area__external_id__in=location_ids)))

        serializer = serializers.SearchAPISerializer({
            'success': True,
            'message': None,
            'everyone': appointments.filter(is_private=False),
            'youonly': appointments.filter(is_private=True).filter(
                attendees__external_id__contains=my_profile.external_id)
        })

        return rest_framework.response.Response(serializer.data)


class Attend(APIView):
    def post(self, request: HttpRequest, fmt=None):
        try:
            my_profile: Profile = self.request.user.profile
        except AttributeError:
            return rest_framework.response.Response(serializers.SearchAPISerializer({
                'success': False,
                'message': 'You are not logged in.',
                'everyone': None,
                'youonly': None
            }).data)

        post_data = json.loads(request.body)
        appointment_id = post_data.get('appointment_id')
        appointment = LunchAppointment.objects.get(external_id=appointment_id)

        appointment.attendees.add(my_profile)

        serializer = serializers.SearchAPISerializer({
            'success': True,
            'updated': True,
            'message': None,
            'everyone': None,
            'youonly': None,
        })
        return rest_framework.response.Response(serializer.data)

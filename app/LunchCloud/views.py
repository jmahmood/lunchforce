# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
import json
import logging

import rest_framework.response
import django.forms
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import RedirectView
from rest_framework.views import APIView

import LunchCloud.forms
from LunchCloud import serializers
from LunchCloud.helpers import date_from_string
from LunchCloud.models import Profile, IntroductionCode, LunchAppointment, Availability, FoodOption, Location
import LunchCloud.models

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
    """Produces a list of events that you are invited to."""

    def get(self, request: HttpRequest, frmt=None):
        try:
            my_profile = self.request.user.profile
        except AttributeError:
            return rest_framework.response.Response(serializers.AppointmentAPISerializer({
                'success': False,
                'message': 'You are not logged in.',
                'appointments': None
            }).data)

        appointments = LunchAppointment.objects.filter(
            status='proposed').filter(
            event_date__gt=datetime.date.today()).filter(
            invitees__external_id__contains=my_profile.external_id).exclude(
            attendees__external_id__contains=my_profile.external_id)

        serializer = serializers.AppointmentAPISerializer({
            'success': True,
            'message': None,
            'appointments': appointments
        })
        return rest_framework.response.Response(serializer.data)


class PublicLunchEvents(APIView):
    """Events that you are _not_ invited to, but are _public_."""

    def get(self, request: HttpRequest, frmt=None):
        try:
            my_profile = self.request.user.profile
        except AttributeError:
            return rest_framework.response.Response(serializers.AppointmentAPISerializer({
                'success': False,
                'message': 'You are not logged in.',
                'appointments': None
            }).data)

        appointments = LunchAppointment.objects.filter(
            status='proposed').filter(
            event_date__gt=datetime.date.today()).exclude(
            invitees__external_id__contains=my_profile.external_id).filter(
            is_private=False)

        serializer = serializers.AppointmentAPISerializer({
            'success': True,
            'message': None,
            'appointments': appointments
        })
        return rest_framework.response.Response(serializer.data)


class MyLunchAppointments(APIView):
    """Returns a list of appointments that you have confirmed that you wish to attend."""

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
    """Allows you to make changes to your profile if you are logged in."""

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
    """Name / email / other information about your profile."""

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
    """List of availability dates"""

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
    """Allows you to add new availability dates.  Automatically deletes dates that are not in this list."""

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
        dates = available_dates.get('date')

        all_dates = {date_from_string(dt) for dt in dates}

        existing_availability = my_profile.availability_set.all()

        # delete all dates that are no longer necessary.
        to_delete = existing_availability.exclude(frm__in=all_dates)
        if to_delete.count() > 0:
            to_delete.delete()

        already_exist = {t.frm.date() for t in existing_availability.filter(frm__in=all_dates)}

        to_create = all_dates - already_exist

        all_availabilities: [Availability] = []

        for dt in to_create:
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
    """A list of food options you can set in your profile / search.  Cachable, rarely changes."""

    def get(self, request: HttpRequest, fmt=None):
        food_options = FoodOption.objects.filter(enabled=True)

        serializer = serializers.FoodOptionAPISerializer({
            'success': True,
            'message': None,
            'food_options': food_options
        })

        return rest_framework.response.Response(serializer.data)


class Locations(APIView):
    """A list of locations you can eat at for your profile / search.  Cachable, rarely changes."""

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
    """Allows you to confirm that you will attend a lunch appointment"""

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


class IntroductionAPI(APIView):
    """Allows you to introduce new people to the site."""

    def post(self, request: HttpRequest, fmt=None):
        try:
            my_profile: Profile = self.request.user.profile
        except AttributeError:
            return rest_framework.response.Response(serializers.IntroductionAPISerializer({
                'success': False,
                'message': 'You are not logged in.',
                'introduction_code': None
            }).data)

        post_data = json.loads(request.body)
        invitee_email: str = post_data.get('invitationEmail')

        try:
            validate_email(invitee_email)
        except django.forms.ValidationError:
            return rest_framework.response.Response(serializers.IntroductionAPISerializer({
                'success': False,
                'message': 'You must include a valid email.',
                'introduction_code': None
            }).data)

        if not (invitee_email.endswith('@salesforce.com') or invitee_email.endswith('@heroku.com')):
            return rest_framework.response.Response(serializers.IntroductionAPISerializer({
                'success': False,
                'message': 'Invitee must have a Salesforce or Heroku email.',
                'introduction_code': None
            }).data)

        introduction = IntroductionCode(
            invited_by=my_profile,
            invitee_email=invitee_email
        )
        introduction.save()

        serializer = serializers.IntroductionAPISerializer({
            'success': True,
            'message': None,
            'introduction_code': introduction.code,
            'email': introduction.invitee_email
        })
        return rest_framework.response.Response(serializer.data)


class Logout(APIView):
    """Allows easy logouts from the API.  """

    def get(self, request, format=None):
        # simply delete the token to force a login
        request.user.auth_token.delete()
        serializer = serializers.LogoutAPISerializer({
            'success': True,
            'error_messages': None
        })
        return rest_framework.response.Response(serializer.data)


class EnrollView(APIView):
    """People with a valid Username / Password can enroll in our services."""

    def post(self, request, format=None):
        # simply delete the token to force a login
        post_data = json.loads(request.body)

        # Validate email / intro code pair.
        try:
            io = IntroductionCode.objects.get(invitee_email__iexact=post_data.get('enrollmentEmail'),
                                              code=post_data.get('enrollmentIntroductionCode'),
                                              used=False)
            io.used = True
            io.save()
        except IntroductionCode.DoesNotExist:
            serializer = serializers.EnrollmentAPISerializer({
                'success': False,
                'message': 'Invalid Introduction Code'
            })
            return rest_framework.response.Response(serializer.data)

        try:
            _ = User.objects.get(username=post_data.get('enrollmentEmail'))
            serializer = serializers.EnrollmentAPISerializer({
                'success': False,
                'message': 'User already registered'
            })
            return rest_framework.response.Response(serializer.data)

        except User.DoesNotExist:
            pass

        new_user = User(email=post_data.get('enrollmentEmail'), username=post_data.get('enrollmentEmail'))
        new_user.set_password(post_data.get('enrollmentPassword'))
        new_user.save()

        new_user_profile = Profile(
            user=new_user,
            invited_by=io.invited_by,
        )

        new_user_profile.save()

        new_user_profile.locations.add(*list(Location.objects.filter(external_id__in=[p.get('id') for p in post_data.get('selectLocation')])))
        new_user_profile.whitelist.add(*list(Location.objects.filter(external_id__in=[p.get('id') for p in post_data.get('selectWhitelist')])))

        serializer = serializers.EnrollmentAPISerializer({
            'success': True,
            'message': None
        })

        return rest_framework.response.Response(serializer.data)



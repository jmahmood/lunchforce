# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
import logging

from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIRequestFactory
from rest_framework.test import force_authenticate

# Create your tests here.
from LunchCloud.helpers import date_from_string
from LunchCloud.models import Profile, FoodOption, Location, LunchAppointment, Availability
from LunchCloud.views import CreateAvailability, MyAvailability


def attendee_meeting_dict(recent_lunch_meetings: {LunchAppointment}) -> {Profile: LunchAppointment}:
    ret = dict.fromkeys([attendee for meeting in recent_lunch_meetings
                         for attendee in meeting.attendees.all()], [])

    for a, m in [(attendee, meeting) for meeting in recent_lunch_meetings for attendee in meeting.attendees.all()]:
        ret[a].append(m)

    return ret

class TestCaseWithProfiles(TestCase):
    def setUp(self):
        super().setUp()
        user_names = ['jack', 'jill', 'john', 'jerry', 'jim']
        korean_lovers = ['kim', 'kang', 'frank']
        multiple_locations = ['Dennis', 'Bart']
        User.objects.bulk_create(
            [User(username=un) for un in user_names + korean_lovers + multiple_locations]
        )
        Location.objects.create(name='Tokyo Test')
        Location.objects.create(name='Koenji Test')
        self.locations = Location.objects.all()

        FoodOption.objects.create(name='Indian')
        FoodOption.objects.create(name='Korean')
        self.food_options = FoodOption.objects.all()

        self.users = User.objects.filter(username__in=user_names)
        self.korean_lover_users = User.objects.filter(username__in=korean_lovers)
        self.multiple_location_users = User.objects.filter(username__in=multiple_locations)

        user_dict = {u.username: u for u in self.users}
        user_dict.update({u.username: u for u in self.korean_lover_users})
        user_dict.update({u.username: u for u in self.multiple_location_users})

        Profile.objects.bulk_create(
            [
                Profile(
                    user=user_dict.get(un),
                )
                for un in user_names + korean_lovers + multiple_locations
            ]
        )

        profiles = Profile.objects.filter(user_id__in=[u.id for u in self.users])
        for p in profiles:
            p.locations.add(self.locations[0])
            p.whitelist.add(self.food_options[0])

        profiles = Profile.objects.filter(user_id__in=[u.id for u in self.multiple_location_users])
        for p in profiles:
            p.locations.add(self.locations[0])
            p.locations.add(self.locations[1])
            p.whitelist.add(self.food_options[0])

        profiles = Profile.objects.filter(user_id__in=[u.id for u in self.korean_lover_users])
        for p in profiles:
            p.locations.add(self.locations[0])
            p.whitelist.add(self.food_options[1])

        self.users = User.objects.filter(username__in=user_names)
        self.korean_lover_users = User.objects.filter(username__in=korean_lovers)
        self.multiple_location_users = User.objects.filter(username__in=multiple_locations)


class TestAvailabilityAPI(TestCaseWithProfiles):

    def testViewBaseCase(self):
        """You should not lose availability dates in February or in December when you update January"""

        available_date = datetime.datetime.today() + datetime.timedelta(days=32)
        available_date = datetime.datetime(year=available_date.year, month=available_date.month, day=1)

        available_date_obj = Availability(
            frm=available_date, until=available_date + datetime.timedelta(hours=1), profile=self.users[0].profile)
        available_date_obj.save()

        factory = APIRequestFactory()

        view = MyAvailability.as_view()
        request = factory.get('/api/my-availability/', format='json')
        force_authenticate(request, user=self.users[0])
        response = view(request)
        self.assertIn(available_date_obj.frm.date(), [date_from_string(d.get('date_str')) for d in response.data.get('availability')])

    def testNoDuplicates(self):
        """A user should not have duplicate date/times in the profile."""

        available = datetime.datetime.today() + datetime.timedelta(days=32)
        available = datetime.datetime(year=available.year, month=available.month, day=1)

        existing_availability = Availability(
            frm=available, until=available + datetime.timedelta(hours=1), profile=self.users[0].profile)
        existing_availability.save()

        dts = ['{0}-{1}-{2}'.format(existing_availability.frm.year,
                                    existing_availability.frm.month,
                                    existing_availability.frm.day)
               for x in range(1, 9)]

        payload = {"month": existing_availability.frm.month,
                   "date": dts}

        logging.debug(repr(payload))

        factory = APIRequestFactory()

        view = CreateAvailability.as_view()
        request = factory.post('/api/update-availability/', payload, format='json')
        force_authenticate(request, user=self.users[0])
        response = view(request)
        self.assertTrue(response.data.get('success'))

        self.assertTrue(Availability.objects.filter(profile=self.users[0].profile).count() == 1)

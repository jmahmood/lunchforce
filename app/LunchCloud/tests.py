# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
import logging
from typing import List, Tuple

import django.db.utils
import itertools
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase

# Create your tests here.
from LunchCloud.forms import RegistrationForm, AvailabilityForm
from LunchCloud.helpers import LunchPerson, LunchAppointmentGroup, FinderBot, AutoInviteBot
from LunchCloud.models import Profile, IntroductionCode, FoodOption, Location, LunchAppointment, Availability
from rest_framework.test import APIRequestFactory
from rest_framework.test import force_authenticate

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

    def testNoDuplicateRecords(self):
        """You should not lose availability dates in February or in December when you update January"""

        available = datetime.datetime.today() + datetime.timedelta(days=32)
        available = datetime.datetime(year=available.year, month=available.month, day=1)

        existing_availability = Availability(
            frm=available, until=available + datetime.timedelta(hours=1), profile=self.users[0].profile)
        existing_availability.save()

        factory = APIRequestFactory()

        view = MyAvailability.as_view()
        request = factory.get('/api/my-availability/', format='json')
        force_authenticate(request, user=self.users[0])
        response = view(request)
        data = response.data
        self.assertIn(existing_availability.frm, [d.date_str for d in data.availability])
        logging.warning(existing_availability.frm in [d.date_str for d in data.availability])




        create_availability_by_api = available + datetime.timedelta(days=32)
        dts = ['{0}-{1}-{2}'.format(create_availability_by_api.year, create_availability_by_api.month, x)
               for x in range(1, 9)]
        logging.warning(dts)

        payload = {"month": create_availability_by_api.month,
                   "date": dts}

        view = CreateAvailability.as_view()
        request = factory.post('/api/update-availability/', payload, format='json')
        force_authenticate(request, user=self.users[0])
        response = view(request)
        logging.warning(response.data)


class InvitationTestCases(TestCaseWithProfiles):
    """Tests that are used with helpers.AutoInviteBot, and with the commandline tool"""

    def setUp(self):
        """
        Must create people who have events available on date (d) and both have don't have confirmed events on the same day.



        :return:
        """
        super().setUp()

    def testCreateAppointmentWithHistory(self):
        # 4 people, 3 people in each group.
        people = self.users[0:4]

        for i, subset in enumerate(itertools.combinations(people, 3)):
            dt = (datetime.datetime.today() - datetime.timedelta(days=i)).date()
            event = LunchAppointment(title='Test Invitation',
                                     general_area=self.locations[0],
                                     event_date=dt,
                                     creator=self.users[0].profile,
                                     min_attendees=2,
                                     max_attendees=5,
                                     status='done')
            event.save()
            event.invitees.add(*[user.profile for user in subset])
            event.attendees.add(*[user.profile for user in subset])

        # add availability for that day.
        available = datetime.datetime.today() + datetime.timedelta(days=1)

        for u in self.users:
            x = Availability(
                frm=available, until=available + datetime.timedelta(hours=1), profile=u.profile)
            x.save()

        aib = AutoInviteBot("{0}-{1}-{2}".format(available.year, available.month, available.day))
        results = aib()
        # Person 4 did not attend any of the previous meetings so he or she should be in here.
        self.assertIn(self.users[4].profile, results[0][1][0].invitees.all())

    def testCreateAppointment(self):
        appointment_date = datetime.datetime.today() + datetime.timedelta(days=45)
        event = LunchAppointment(title='TestInvitations',
                                 general_area=self.locations[0],
                                 event_date=appointment_date.date(),
                                 creator=self.users[0].profile,
                                 min_attendees=2,
                                 max_attendees=5,
                                 status='proposed')
        event.save()
        event.invitees.add(*[u.profile for u in self.users[0:3]])
        event.attendees.add(self.users[0].profile)

        # add availability for that day.
        for u in self.users:
            x = Availability(
                frm=appointment_date, until=appointment_date + datetime.timedelta(hours=1), profile=u.profile)
            x.save()

        aib = AutoInviteBot("{0}-{1}-{2}".format(appointment_date.year, appointment_date.month, appointment_date.day))
        aib()

        updated_event = LunchAppointment.objects.get(pk=event.pk)

        self.assertEqual(len(updated_event.invitees.all()), 4)


class BinAlgorithmTestCases(TestCaseWithProfiles):
    def setUp(self):
        super().setUp()

    def testBaseCase(self):
        lunch_people = [LunchPerson.factory(u.profile, {}, {})
                        for u in self.users]

        for lp in lunch_people:
            lp.is_noob = False

        lunch_groups = []

        finder_bot = FinderBot(lunch_people, lunch_groups)
        updated_lunch_groups, _ = finder_bot()

        # updated_lunch_groups = make_groups(lunch_people, lunch_groups)
        self.assertEquals(len(updated_lunch_groups), 1)
        for grp in updated_lunch_groups:
            self.assertEquals(len(grp.people), 4)

    def testThreeNoobs(self):
        lunch_people = [LunchPerson.factory(u.profile, {}, {}) for u in self.users]

        for lp in lunch_people:
            lp.is_noob = False

        for lp in lunch_people[0:3]:
            lp.is_noob = True

        finder_bot = FinderBot(lunch_people, [])
        updated_lunch_groups, _ = finder_bot()
        self.assertEquals(len(updated_lunch_groups), 2)

    def testLocationOverlap(self):

        lunch_people = [LunchPerson.factory(u.profile, {}, {})
                        for u in self.multiple_location_users]

        for lp in lunch_people:
            lp.is_noob = False

        finder_bot = FinderBot(lunch_people, [])
        updated_lunch_groups, _ = finder_bot()
        self.assertEquals(len(updated_lunch_groups), 1)

    def testPreexistingEvent(self):

        lunch_people = [LunchPerson.factory(u.profile, {}, {})
                        for u in self.users]

        for lp in lunch_people:
            lp.is_noob = False

        pre_existing_lunch_group = LunchAppointmentGroup(
            people=lunch_people[0:3]
        )
        pre_existing_lunch_group.original = 'abc'

        finder_bot = FinderBot(lunch_people, [pre_existing_lunch_group])
        updated_lunch_groups, _ = finder_bot()

        self.assertEquals(len(updated_lunch_groups), 1)
        self.assertEquals(updated_lunch_groups[0].original, 'abc')

    def testPreexistingEventAndPastHistory(self):

        app = LunchAppointment(
            event_date=(datetime.datetime.today() - datetime.timedelta(days=10)).date(),
            min_attendees=2,
            max_attendees=5,
            title='Test Event',
            general_area=self.locations[0],
            creator=self.users[0].profile,
            status='Done'
        )
        app.save()
        app.attendees.add(self.users[0].profile, self.users[3].profile)

        my_recent_lunch_meetings = attendee_meeting_dict([app])

        lunch_people = [LunchPerson.factory(u.profile, my_recent_lunch_meetings, {})
                        for u in self.users]

        for lp in lunch_people:
            lp.is_noob = False

        pre_existing_lunch_group = LunchAppointmentGroup(
            people=lunch_people[0:3]
        )
        pre_existing_lunch_group.original = 'abc'

        finder_bot = FinderBot(lunch_people, [pre_existing_lunch_group])
        updated_lunch_groups, _ = finder_bot()

        self.assertEquals(len(updated_lunch_groups), 2)
        self.assertEquals(updated_lunch_groups[0].original, 'abc')

        # You've had lunch with the dude in the group a while back, so give someone else a turn.
        self.assertNotIn(self.users[3].profile, [p.original for p in updated_lunch_groups[0].people])

    def testMultiplePreexistingEvent(self):
        u = User(username='GRUG')
        u.save()
        p = Profile(user=u, invited_by=self.users[0].profile)
        p.save()
        p.locations.add(self.locations[0])
        p.whitelist.add(self.food_options[0])

        lp = LunchPerson.factory(p, {}, {})

        already_at_lunch_people = [LunchPerson.factory(u.profile, {}, {})
                                   for u in self.users]

        for already_lunching in already_at_lunch_people:
            already_lunching.is_noob = False

        pre_existing_lunch_groups = [LunchAppointmentGroup(
            people=already_at_lunch_people[0:3],
        ), LunchAppointmentGroup(
            people=already_at_lunch_people[3:5],
        )]

        finder_bot = FinderBot([lp], pre_existing_lunch_groups)
        updated_lunch_groups, _ = finder_bot()

        for ulg in updated_lunch_groups:
            # new dude gets added to the smaller event, making it 3-3
            self.assertEquals(len(ulg), 3)

    def testOverlappingTastes(self):
        for u in self.users[0:2]:
            for wl in u.profile.whitelist.all():
                u.profile.whitelist.remove(wl)

            u.profile.whitelist.add(self.food_options[1])

        lunch_people = [LunchPerson.factory(u.profile, {}, {}) for u in self.users[0:4]]

        for lp in lunch_people:
            lp.is_noob = False

        finder_bot = FinderBot(lunch_people, [])
        updated_lunch_groups, _ = finder_bot()

        for ulg in updated_lunch_groups:
            # new dude gets added to the smaller event, making it 3-3
            self.assertEquals(len(ulg), 2)

    def testMultipleOverlappingTastes(self):

        lunch_people = [LunchPerson.factory(u.profile, {}, {})
                        for u in self.users[0:2]]

        lunch_people = lunch_people + [LunchPerson.factory(u.profile, {}, {}) for u in self.korean_lover_users[0:3]]

        for lp in lunch_people:
            lp.is_noob = False

        finder_bot = FinderBot(lunch_people, [])
        updated_lunch_groups, _ = finder_bot()

        self.assertEquals(2, len(updated_lunch_groups))

        total_members = [len(ulg) for ulg in updated_lunch_groups]
        self.assertIn(2, total_members)
        self.assertIn(3, total_members)


class AvailabilityFormTests(TestCase):
    def testValidOrder(self):
        frm: AvailabilityForm = AvailabilityForm(
            {
                'frm': datetime.datetime.now(),
                'until': datetime.datetime.now() + datetime.timedelta(hours=5)
            }
        )
        self.assertTrue(frm.is_valid())

    def testInvalidOrder(self):
        frm: AvailabilityForm = AvailabilityForm(
            {
                'frm': datetime.datetime.now(),
                'until': datetime.datetime.now() + datetime.timedelta(hours=-5)
            }
        )
        self.assertFalse(frm.is_valid())


class RegistrationFormTests(TestCase):
    def setUp(self):
        super().setUp()
        self.u = User.objects.create(username='jmahmood')
        self.p = Profile.objects.create(user=self.u)
        self.ft = FoodOption.objects.create(name='Halal')

    def testValidRegistration(self):
        ic: IntroductionCode = IntroductionCode.objects.create(
            invited_by=self.p,
            code='123',
            used=False
        )

        frm: RegistrationForm = RegistrationForm(
            {'invitation_code': ic.code,
             'email': 'address@address.com',
             'foods': [self.ft.pk]
             }
        )
        self.assertTrue(frm.is_valid())

    def testNoReusingInvitationCodes(self):
        ic: IntroductionCode = IntroductionCode.objects.create(
            invited_by=self.p,
            code='456',
            used=True
        )

        frm: RegistrationForm = RegistrationForm(
            {'invitation_code': ic.code,
             'email': 'address@address.com',
             'foods': [self.ft.pk]
             }
        )
        self.assertFalse(frm.is_valid())

    def testInvalidRegistration(self):
        frm: RegistrationForm = RegistrationForm(
            data={'invitation_code': 'fakecode!',
                  'email': 'address@address.com',
                  'foods': [self.ft.pk]
                  }
        )

        self.assertFalse(frm.is_valid())


class ProfileMethodTests(TestCase):
    def setUp(self):
        super().setUp()
        u = User.objects.create(username='jmahmood')
        Profile.objects.create(user=u)

    def testOneToOneOnly(self):
        profiles = Profile.objects.all()

        for p in profiles:
            with self.assertRaises(django.db.utils.IntegrityError):
                Profile.objects.create(user=p.user)

    def testYouMustBeInvited(self):
        u = User.objects.create(username='flanders')
        p = Profile(
            user=u
        )

        with self.assertRaises(ValidationError):
            p.save()

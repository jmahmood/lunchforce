# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
import logging

import django.db.utils
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase

# Create your tests here.
from LunchCloud.forms import RegistrationForm, AvailabilityForm
from LunchCloud.helpers import make_groups, LunchPerson, LunchAppointmentGroup, attendee_meeting_dict, FinderBot
from LunchCloud.models import Profile, IntroductionCode, FoodOption, Location, LunchAppointment


class MatchingBaseCase(TestCase):
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

    def testBaseCase(self):
        lunch_people = [LunchPerson.factory(u.profile, {})
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
        lunch_people = [LunchPerson.factory(u.profile, {}) for u in self.users]

        for lp in lunch_people:
            lp.is_noob = False

        for lp in lunch_people[0:3]:
            lp.is_noob = True

        finder_bot = FinderBot(lunch_people, [])
        updated_lunch_groups, _ = finder_bot()
        self.assertEquals(len(updated_lunch_groups), 2)

    def testLocationOverlap(self):

        lunch_people = [LunchPerson.factory(u.profile, {})
                        for u in self.multiple_location_users]

        for lp in lunch_people:
            lp.is_noob = False

        finder_bot = FinderBot(lunch_people, [])
        updated_lunch_groups, _ = finder_bot()
        self.assertEquals(len(updated_lunch_groups), 1)

    def testPreexistingEvent(self):

        lunch_people = [LunchPerson.factory(u.profile, {})
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

        lunch_people = [LunchPerson.factory(u.profile, my_recent_lunch_meetings)
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

        lp = LunchPerson.factory(p, {})

        already_at_lunch_people = [LunchPerson.factory(u.profile, {})
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

        lunch_people = [LunchPerson.factory(u.profile, {}) for u in self.users[0:4]]

        for lp in lunch_people:
            lp.is_noob = False

        finder_bot = FinderBot(lunch_people, [])
        updated_lunch_groups, _ = finder_bot()

        for ulg in updated_lunch_groups:
            # new dude gets added to the smaller event, making it 3-3
            self.assertEquals(len(ulg), 2)

    def testMultipleOverlappingTastes(self):

        lunch_people = [LunchPerson.factory(u.profile, {})
                        for u in self.users[0:2]]

        lunch_people = lunch_people + [LunchPerson.factory(u.profile, {}) for u in self.korean_lover_users[0:3]]

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

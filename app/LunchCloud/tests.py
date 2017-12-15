# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import forms
from django.test import TestCase
import django.db.utils
import datetime

# Create your tests here.
from LunchCloud.forms import RegistrationForm, AvailabilityForm
from LunchCloud.models import Profile, InvitationCode, FoodOption


class AvailabilityFormTests(TestCase):
    def testValidOrder(self):
        frm:AvailabilityForm = AvailabilityForm(
            {
                'frm': datetime.datetime.now(),
                'until': datetime.datetime.now() + datetime.timedelta(hours=5)
            }
        )
        self.assertTrue(frm.is_valid())

    def testInvalidOrder(self):
        frm:AvailabilityForm = AvailabilityForm(
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
        ic: InvitationCode = InvitationCode.objects.create(
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
        ic: InvitationCode = InvitationCode.objects.create(
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

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models


class FoodType(models.Model):

    def __str__(self):
        return self.name

    name = models.CharField(max_length=80, verbose_name="Type of Food", default='')
    enabled = models.BooleanField(default=True)


class Availability(models.Model):
    frm = models.DateTimeField()
    until = models.DateTimeField()


class Profile(models.Model):

    def __str__(self):
        return '{0} - Profile'.format(self.user.username)

    user = models.OneToOneField(User, unique=True)

    # Email needs to be saved to user.email.
    invited_by = models.ForeignKey("self", null=True, blank=True)
    blacklist = models.ManyToManyField(FoodType, blank=True, related_name='blacklisted_by')
    whitelist = models.ManyToManyField(FoodType, related_name='whitelisted_by')
    availability = models.ManyToManyField(Availability, blank=True)

    def clean(self):
        # Don't allow draft entries to have a pub_date.
        if self.user.username != 'jmahmood' and self.invited_by == None:
            raise ValidationError(_('You must be invited by someone.'))


class InvitationCode(models.Model):
    invited_by = models.ForeignKey(Profile)
    code = models.CharField(max_length=50, verbose_name='Invitation Code')
    used = models.BooleanField(default=False)

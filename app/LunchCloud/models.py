# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import gettext

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models

_ = gettext.gettext

_THESEED = 'jmahmood'  # The username of the original user who invites everyone.


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
    whitelist = models.ManyToManyField(FoodType, blank=True, related_name='whitelisted_by')
    availability = models.ManyToManyField(Availability, blank=True)

    def clean(self):
        if self.user.username != _THESEED and self.invited_by is None:
            raise ValidationError(_('You must be invited by someone.'))

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        try:
            self.clean()
            super().save(force_insert, force_update, using, update_fields)
        except ValidationError as e:
            raise e


class LunchEvents(models.Model):
    event_date = models.DateField()
    frm = models.TimeField()
    until = models.TimeField()
    invitees = models.ManyToManyField(Profile, related_name='invited_to')
    attendees = models.ManyToManyField(Profile, blank=True, related_name='attended')
    min_attendees = models.SmallIntegerField('Min number of attendees')
    max_attendees = models.SmallIntegerField('Max number of attendees')
    description = models.TextField('Event Description')
    creator = models.ForeignKey(Profile)
    allow_evaluation = models.BooleanField(default=False)
    status = models.CharField(max_length=40, choices=[
        (_('Proposed'), 'proposed'),
        (_('Confirmed'), 'confirmed'),
        (_('Rejected'), 'rejected'),
        (_('Awaiting Evaluation'), 'awaiting'),
        (_('Done'), 'done')], default='proposed')


class InvitationCode(models.Model):
    invited_by = models.ForeignKey(Profile)
    code = models.CharField(max_length=50, verbose_name='Invitation Code', unique=True)
    used = models.BooleanField(default=False)

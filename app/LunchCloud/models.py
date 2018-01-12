# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import gettext
import uuid

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models

_ = gettext.gettext

_THESEED = 'jmahmood'  # The username of the original user who invites everyone.

def uuid_str():
    return str(uuid.uuid4())


class FoodOption(models.Model):
    def __str__(self):
        return self.name
    external_id = models.CharField(max_length=80, default=uuid_str)
    name = models.CharField(max_length=80, verbose_name="Type of Food", default='')
    enabled = models.BooleanField(default=True)


class Location(models.Model):

    def __str__(self):
        return self.name

    external_id = models.CharField(max_length=80, default=uuid_str)
    name = models.CharField(max_length=80, verbose_name="Easy-to-understand name of a local landmark")
    enabled = models.BooleanField(default=True)


class Profile(models.Model):
    """
    The profile is used to store food preferences.

    We may change this in the future, as we want to eventually use SSO,
    and it isn't clear to me if we can do so with User.
    """

    def __str__(self):
        return _('{0} - Profile').format(self.user.username)

    user = models.OneToOneField(User, unique=True)

    external_id = models.CharField(max_length=80, default=uuid_str)
    invited_by = models.ForeignKey("self", null=True, blank=True)
    locations = models.ManyToManyField(Location, blank=True, related_name='used_by')
    blacklist = models.ManyToManyField(FoodOption, blank=True, related_name='blacklisted_by')
    whitelist = models.ManyToManyField(FoodOption, blank=True, related_name='whitelisted_by')

    def clean(self):
        if self.user.username != _THESEED and self.invited_by is None:
            raise ValidationError(_('You must be invited by someone.'))

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        try:
            self.clean()
            super().save(force_insert, force_update, using, update_fields)
        except ValidationError as e:
            raise e


class Availability(models.Model):
    frm = models.DateTimeField()
    until = models.DateTimeField()
    profile = models.ForeignKey(Profile)

    class Meta:
        unique_together = ('frm', 'profile')


class LunchAppointment(models.Model):
    external_id = models.CharField(max_length=80, default=uuid_str)
    event_date = models.DateField()
    frm = models.TimeField(null=True, blank=True)
    until = models.TimeField(null=True, blank=True)
    invitees = models.ManyToManyField(Profile, related_name='invited_to')
    attendees = models.ManyToManyField(Profile, blank=True, related_name='confirmed')
    min_attendees = models.SmallIntegerField(_('Min attendees'))
    max_attendees = models.SmallIntegerField(_('Max attendees'))
    title = models.CharField(_('Event Title'), max_length=80)
    description = models.TextField(_('Event Description'))
    location = models.CharField(max_length=80)
    general_area = models.ForeignKey(Location)
    creator = models.ForeignKey(Profile)
    allow_evaluation = models.BooleanField(default=False)
    is_private = models.BooleanField(default=False)
    status = models.CharField(max_length=40, choices=[
        (_('Proposed'), 'proposed'),
        (_('Confirmed'), 'confirmed'),
        (_('Rejected'), 'rejected'),
        (_('Awaiting Evaluation'), 'awaiting'),
        (_('Done'), 'done')], default='proposed')

    def __str__(self):
        return "{0} - {1} ({2})".format(
            self.title, self.location, self.creator.user.username
        )


class IntroductionCode(models.Model):
    invitee_email = models.EmailField()
    invited_by = models.ForeignKey(Profile)
    code = models.CharField(default=uuid_str, max_length=50, verbose_name=_('Invitation Code'), unique=True)
    used = models.BooleanField(default=False)

    def __str__(self):
        return "{0} - {1} ({2})".format(self.invitee_email, self.invited_by.user.username, self.used)

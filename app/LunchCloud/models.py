# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import gettext
import logging
import random
import uuid

import names
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models

_ = gettext.gettext

_THESEED = 'jmahmood'  # The username of the original user who invites everyone.


def report_on_fairness(person, all_people, context):
    """
    Generates a text report on a person who was left out of a lunch event, despite potentially having people there that
    he did not despise.
    """

    return """{0} signed up for lunch on {1} but this algo could not find him anyone.
{0} previously was matched on {2}, going out with {3}.
{0} currently hates {4}.
The people who signed up for lunch on {1} were {5}.""".format(
        person.name,
        context.usage_history,
        context.last_usage,
        ','.join(context.last_usage_partners),
        ','.join(person.hates),
        ','.join(all_people)
    )


class LunchPerson:
    id = ''
    name = ''
    is_noob = False
    food_likes = set()
    people_met = set()
    hates = set()
    food_types = ['Japanese', 'Chinese', 'Indian', 'American', 'Hamburger', 'Pizza']

    def __str__(self):
        return self.name

    def __init__(self, person_id, name, is_noob, food_likes, people_met, hates) -> None:
        super().__init__()
        self.id = person_id
        self.name = name
        self.is_noob = is_noob
        self.food_likes = food_likes
        self.people_met = people_met
        self.hates = hates

    def recently_met(self, person):
        return self.people_met is not None and person.id not in self.people_met

    @staticmethod
    def factory():
        return LunchPerson(
            person_id=str(uuid.uuid4()),
            name=names.get_full_name(),
            is_noob=(random.randint(0, 100) % 25 > 0),
            food_likes=set(LunchPerson.food_types),
            people_met=None,
            hates=None
        )

    @staticmethod
    def factory_different_food_likes():
        p = LunchPerson.factory()
        p.food_likes = set(LunchPerson.food_types[random.randint(0, 6)] for _ in random.randint(1, 4))
        return p


class LunchGroup:
    people: [LunchPerson] = []

    def __str__(self) -> str:
        return ','.join([p.name for p in self.people])

    def __len__(self):
        return len(self.people)

    def __getitem__(self, item):
        return self.people[item]

    def __hash__(self):
        logging.warning(','.join([p.id for p in sorted(self.people, key=id)]))
        return hash(','.join([p.id for p in sorted(self.people, key=id)]))

    def __init__(self, people=None) -> None:
        super().__init__()
        if people is None:
            self.people = []
        else:
            self.people = people

    def __iter__(self):
        self.iter_n = -1
        return self

    def __next__(self):
        self.iter_n += 1
        try:
            return self.people[self.iter_n]
        except IndexError:
            raise StopIteration

    def ids(self):
        return {p.id for p in self.people}

    def food_likes(self):
        food_likes = set(self.people[0].food_likes)
        for p in self.people:
            food_likes.intersection(p.food_likes)

        return food_likes

    def append(self, other):
        ids = [p.id for p in self.people]
        if other.id not in ids:
            self.people.append(other)


def one_noob_max(person, group: LunchGroup):
    group_noob_count = len([grp_p.is_noob for grp_p in group if grp_p.is_noob])
    return person.is_noob or group_noob_count > 0


def no_haters(person, group: LunchGroup):
    return person.hates is None or len(set(person.hates).intersection(group.ids())) > 0


def flatten(list_of_lists):
    return set(sum(list_of_lists, []))


def make_groups(people: set):
    """
    Based on Greedy Bin Packing Algorithm
        inviolable rules:
        -> You cannot go out with someone you hate.
        -> max size 4

        nice to have:
        -> If you can join more than one group, join the smallest group there is.
        -> everyone has at least one type of food they like in common
        -> we haven't recently (within 2 months) met each other
        -> only one new person per group

    rules = [fn1, fn2]
    nice_to_have = [fn4, fn5, fn6...]
    groups = []

    fn(rules, nice_to_have, groups, people):
        for person in people:
            compatible_groups = filter(groups, person, rules)
            compatible_groups = filter(compatible_groups, person, nice_to_have)

            if len(compatible_groups) > 0
                compatible_groups[0].add(person)
            else:
                groups.add([person])

        solitary_people = filter_solitary(groups)
        if nice_to_have > 0 and len(solitary_people) > 0:
            nice_to_have.pop() # remove a rule.
            return fn(rules, nice_to_have, groups, people)

        return groups, solitary_people

    -----

    :param people:
    :return:
    """

    inviolable_rules = lambda prsn, grp: len(grp) < 4 and no_haters(prsn, grp)
    x = set()
    nice_to_have = [one_noob_max,
                    # ^^ 1 noob max
                    lambda prsn, grp: len(prsn.food_likes.intersection(grp.food_likes())) > 0,
                    # ^^ You share a liked food with someone in the group.  Probably needs to narrow down
                    lambda prsn, grp: True not in [prsn.recently_met(grp_p) for grp_p in grp],
                    # ^^ You haven't recently met anyone in the group.
                    ]
    groups: set = set()

    lonely_people = list(people)
    lonely_people.sort(key=lambda per: per.is_noob)

    while len(lonely_people) > 0 and len(nice_to_have) > 0:
        for p in lonely_people:
            compatible_groups = []
            logging.warning("Searching through groups for {0}".format(p.name))
            for g in groups:

                compatible = inviolable_rules(p, g)  # This must, at all times, be true.

                for r in nice_to_have:
                    compatible = compatible and r(p, g)  # These slowly become less important.

                if compatible:
                    compatible_groups.append(g)

            if len(compatible_groups) > 0:
                logging.warning("Appending to compatible group.")
                compatible_groups.sort(key=lambda c_gx: len(c_gx.people), reverse=True)
                compatible_groups[0].append(p)  # Append to smallest compatible group
            else:
                logging.warning("No compatible groups; creating new one.")
                groups.add(LunchGroup([p]))

        valid_groups = [grp for grp in groups if len(grp.people) > 1]
        invalid_groups = [grp for grp in groups if grp not in valid_groups]

        # Find out the social misfits and troublemakers who are left over.
        lonely_people = [p[0] for p in invalid_groups]
        groups = set(valid_groups)
        logging.warning(lonely_people)

        nice_to_have.pop()  # get rid of a rule

    # Why are you lonely, little man?  Send a mail to explain how it is hard to match people who have
    # impossible requirements.
    return groups



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
    locations = models.ManyToManyField(Location, blank=True, related_name='locations')
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
    invited_by = models.ForeignKey(Profile)
    code = models.CharField(default=uuid_str, max_length=50, verbose_name=_('Invitation Code'), unique=True)
    used = models.BooleanField(default=False)

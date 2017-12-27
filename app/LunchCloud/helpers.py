"""
Basic helper functions for LunchCloud

Focused mostly on auto-inviting people who are available on a date (and don't have a lunch meeting) to an event.
"""
import datetime
import logging
from types import FunctionType
from typing import List, Dict, Tuple, Iterable

from LunchCloud.models import Profile, LunchAppointment, Location


def date_from_string(dt) -> datetime.date:
    """Used to convert Javascript dates to Python dates.  We use this to avoid overhead with timezones for now."""
    dt = dt.split('T')[0]
    y, m, d = dt.split('-')
    return datetime.date(year=int(y), month=int(m), day=int(d))


def report_on_fairness(person, all_people, context) -> str:
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
    """
    This is an adaptor that is used to convert a Profile object into an object that can be easily used with
    the Invitation generator

    @TODO: Can we integrate these into the profile object itself, or create a different inherited version of the
    profile object that can be used for this same purpose?
    """
    id = ''
    name = ''
    is_noob = False
    food_likes = set()
    people_met = set()
    hates = set()
    food_types = ['Japanese', 'Chinese', 'Indian', 'American', 'Hamburger', 'Pizza']
    original: Profile = None

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
        """If you have recently met someone, we try to reduce the chance you meet them again."""
        if self.people_met is None or person.id not in self.people_met:
            return False
        return True

    @staticmethod
    def factory(person: Profile, recent_lunches: Dict[Profile, List[LunchAppointment]],
                lunch_stats: Dict[Profile, int]):
        """Generates """
        lunch_attendees = (x.attendees.all() for x in recent_lunches.get(person, []))
        people_met: set = {attendee.external_id for attendee_l in lunch_attendees for attendee in attendee_l}

        logging.debug("""Creating a LunchPerson object.
Name: {0}
People Met: {1}
Lunch Stats: {2} (Used to determine Noobness if not overridden)
""".format(person.user.username, ','.join(list(people_met)), lunch_stats.get(person, 0)))

        lp = LunchPerson(
            person_id=person.external_id,
            name=person.user.username,
            is_noob=lunch_stats.get(person, 0) == 0,
            food_likes=set(person.whitelist.all()),
            people_met=people_met,
            hates=None
        )

        lp.original = person
        return lp


class LunchAppointmentGroup:
    """A class used to simplify the use of LunchAppointments for the application."""
    people: [LunchPerson] = []  # All people invited or attending the event.
    is_private = False
    original: LunchAppointment = None

    def __str__(self) -> str:
        return ', '.join(['{0} ({1})'.format(p.name, p.is_noob) for p in self.people])

    def __len__(self):
        return len(self.people)

    def __getitem__(self, item):
        return self.people[item]

    def __init__(self, people=None) -> None:
        super().__init__()
        if people is None:
            self.people = []
        else:
            self.people = people

    def __iter__(self):
        self.iter_n = -1
        return self

    def __next__(self) -> LunchPerson:
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

    @staticmethod
    def factory(lunch_appointment: LunchAppointment, recent_lunch_meetings, historical_lunch_stats):
        """Convert attendees of an event to lunch people, used by AutoInviteBot to start the FinderBot"""
        people = [LunchPerson.factory(p, recent_lunch_meetings, historical_lunch_stats) for p in lunch_appointment.invitees.all()]
        ret = LunchAppointmentGroup()
        ret.people = people
        ret.is_private = lunch_appointment.is_private
        ret.original = lunch_appointment
        return ret


def one_noob_max(person: LunchPerson, group: LunchAppointmentGroup):
    """We want to try to limit the number of new people in each lunch group in order to allow them to pick up on
    social conventions"""
    group_noob_count = len([grp_p.is_noob for grp_p in group if grp_p.is_noob])
    logging.debug("Found {0} noobs in group {1}".format(group_noob_count, group.__str__()))
    return not person.is_noob or person.is_noob and group_noob_count == 0


def no_gate_crashing(person: LunchPerson, group: LunchAppointmentGroup):
    """You cannot join a private meeting if you are not invited"""
    return not group.is_private or person.original in [p.original for p in group.people]


def no_haters(person: LunchPerson, group: LunchAppointmentGroup):
    """In the future, we will allow hatred to be """
    return person.hates is None or len(set(person.hates).intersection(group.ids())) > 0


def fairness_sort(lonely_people: Iterable[LunchPerson]):
    """
    People who are higher in priority should be closer to the front of this list, people lower in priority should be at
    the back.
    :param lonely_people:
    :return:
    """
    return sorted(lonely_people, key=lambda per: per.is_noob, reverse=True)


def no_recent_meetings(person: LunchPerson, group: LunchAppointmentGroup):
    """Goes through all invitees for an event and checks if you have met any of them recently.
    Returns True if you haven't met anyone in the group recently. (Diversity)"""
    return True not in (person.recently_met(invitee) for invitee in group)


class FinderBot:
    """
    Implements an algorithm to find compatible groups, or to generate new ones, for users passed to the application.
    """

    def __init__(self, people: List[LunchPerson], groups: List[LunchAppointmentGroup]) -> None:
        super().__init__()
        self.people: List[LunchPerson] = people
        self.groups: List[LunchAppointmentGroup] = groups
        self.lonely_people: List[LunchPerson] = self.filter_out_invitees()
        self.lonely_people: List[LunchPerson] = self.fairness_sort()
        self.nice_to_have_rules: List[Tuple[FunctionType, str, str]] = [
            (lambda prsn, grp: len(prsn.food_likes.intersection(grp.food_likes())) > 0, 'Common Interests', 'You must have a food like in common'),
            (no_recent_meetings, 'Freshness', 'You should be meeting new people'),
            (one_noob_max, 'Noobs!', 'Only want 1 Noob per group, if possible.')
        ]

        self.inviolable_rules: List[Tuple[FunctionType, str, str]] = [
            (lambda prsn, grp: len(grp) < 4, 'Group size', 'Groups should have 4 people max.'),
            (no_haters, 'No haters', 'You should not eat with someone you hate.'),
            (no_gate_crashing, 'Gate Crashing', 'You should not barge into a private event.')
        ]

        self.__iter = 0

    def __call__(self, *args, **kwargs) -> Tuple[List[LunchAppointmentGroup], List[LunchPerson]]:
        """
        Calculates the groups that can be done and returns the list, along with people who could not be matched.

        :param args:
        :param kwargs:
        :return:
        """
        if self.__already_called():
            raise InterruptedError('This already been run.')
        while self.should_keep_looking():
            # Return product is null; only interested in side effect.  Haskellers beware.
            [self.add_to_compatible_group(x) for x in self.lonely_people]
            self.groups = self.filter_out_invalid_groups()
            self.lonely_people = self.filter_out_invitees()

        return self.groups, self.lonely_people

    def __already_called(self) -> bool:
        """
        Prevents the FinderBot object from being executed more than once.

        :return:
        """
        self.__iter += 1
        return self.__iter > 1

    def should_keep_looking(self) -> bool:
        """
        Examines the number of lonely people and removes optional rules as necessary to seat them.

        If True, it means there are still more lonely people and we can still reduce the number of rules we have.

        :return:
        """
        if len(self.lonely_people) == 0:
            logging.debug("No lonely people.  Returning.")
            return False
        if self.__iter > 1:
            try:
                self.nice_to_have_rules.pop()
                logging.debug("Relaxing rules.")
            except IndexError:
                logging.debug("No more rules to relax.")
                return False

        self.__iter += 1
        return True

    def add_to_compatible_group(self, p: LunchPerson):
        """
        Sorts compatible groups by the number of attendees and adds the lonely person to the smallest lunch possible.

        :param p:
        :return:
        """
        compatible_groups = sorted(
            [g for g in self.groups if self.is_compatible(p, g)],
            key=lambda c_gx: len(c_gx.people))

        try:
            compatible_groups[0].append(p)
        except IndexError:
            logging.debug("No compatible groups found, creating new one.")
            self.groups.append(LunchAppointmentGroup([p]))

    def filter_out_invalid_groups(self) -> List[LunchAppointmentGroup]:
        """Private groups can have only one person invited, as they may be assembling people.
        All public groups must have more than 1 person invited."""
        return [group for group in self.groups if group.is_private or len(group.people) > 1]

    def filter_out_invitees(self) -> List[LunchPerson]:
        """We do not automatically add people to multiple events."""
        already_invited = [person.id for g in self.groups for person in g.people]
        return fairness_sort([p for p in self.people if p.id not in already_invited])

    def fairness_sort(self) -> List[LunchPerson]:
        """We do not automatically add people to multiple events."""
        return sorted(self.lonely_people, key=lambda per: per.is_noob, reverse=True)

    def is_compatible(self, person: LunchPerson, grp: LunchAppointmentGroup) -> bool:
        """
        Checks to see if the Person is compatible with the group given the currently set nice-to-have rules and all
        of the inviolable rules.

        :param person:
        :param grp:
        :return:
        """
        rule_format = """{0}: {1} ({2})\n"""
        report_card = "\nChecking compatibility of {0} (is noob: {2}) for {1}\n".format(str(person), str(grp), person.is_noob)
        ret = True

        for rule, name, explanation in self.inviolable_rules + self.nice_to_have_rules:
            compatible = rule(person, grp)
            report_card += rule_format.format(name, compatible, explanation)
            if not compatible:
                ret = False

        report_card += "\nResult: {0} ---\n".format(ret)
        logging.info(report_card)

        return ret


class AutoInviteBot:
    """Used by cupid to generate a set of invitations for people with an open lunch on a specific date."""

    def __init__(self, dt: str):
        self.date = date_from_string(dt)
        self.creator = Profile.objects.all()[0]

        self.people = Profile.objects.filter(
            availability__frm__year=self.date.year,
            availability__frm__month=self.date.month,
            availability__frm__day=self.date.day).exclude(
            confirmed__event_date__year=self.date.year,
            confirmed__event_date__month=self.date.month,
            confirmed__event_date__day=self.date.day)

        self.all_locations = Location.objects.filter(used_by__in=self.people).distinct()
        # self.all_locations = set([l for locations in self.people.locations.all() for l in locations])

        """Lunch appointments that already exist for the date (which we may wish to add people to)"""
        self.preexisting_lunch_appointments = LunchAppointment.objects.filter(
            event_date=self.date).filter(general_area__in=self.all_locations)

        """Creates a list of all recent appointments / lunches that someone went on.
        This is used to de-prioritize future lunches so other people can have a turn """
        __recent_lunch_appointments = LunchAppointment.objects.filter(
            event_date__lte=datetime.date.today()).filter(
            attendees__in=self.people)

        self.recent_historical_appointments = {p: __recent_lunch_appointments.filter(
            attendees=p).filter(event_date__gte=(datetime.datetime.now() - datetime.timedelta(days=14)).date())

                                               for p in self.people}

        self.all_historical_appointments = {
            p: len(__recent_lunch_appointments.filter(attendees=p)) for p in self.people}
        logging.warning(self.description())

    def description(self):
        """

        :return:
        """

        return """
Lonely People: {0}
Locations: {1}
Recent Appointments: {2}
Preexisting_appointments: {3}""".format(','.join([str(p) for p in self.people]),
                                        ','.join([str(l) for l in self.all_locations]),
                                        repr(self.recent_historical_appointments),
                                        repr(self.preexisting_lunch_appointments))

    def __call__(self, *args, **kwargs) -> List[Tuple[Location, List[LunchAppointment],
                                                      List[LunchAppointment], List[LunchAppointment]]]:
        # {'location': '', 'all': '', 'new': '', 'old': ''} ?
        ret = []

        for location in self.all_locations:

            lunch_appointment_groups = self.generate_appointment_groups(location)
            new_events = self.save_new_lunch_appointments(
                [lag for lag in lunch_appointment_groups if lag.original is None], location)
            updated_events = self.update_old_lunch_appointments(
                [lag for lag in lunch_appointment_groups if lag.original is not None])

            ret.append((location, new_events + updated_events, new_events, updated_events))

        return ret

    def update_old_lunch_appointments(self, preexisting_lunch_appointment_groups) -> List[LunchAppointment]:
        """Accepts a list of groups that have had a change in their invitees"""
        ret = []
        for g in preexisting_lunch_appointment_groups:
            profile_external_ids = [p.id for p in g.people]
            to_add = self.people.filter(external_id__in=profile_external_ids)
            if to_add.count() > 0:
                g.original.invitees.add(*to_add)
                self.people = self.people.exclude(profile__in=to_add)
                ret.append(g)
        return ret

    def save_new_lunch_appointments(self, new_lunch_appointment_groups, location) -> List[LunchAppointment]:
        """Generates completely new Lunch Appointments for new requests."""
        ret = []
        for g in new_lunch_appointment_groups:
            appointment = LunchAppointment(
                    event_date=self.date,
                    min_attendees=2,
                    max_attendees=5,
                    title='Lunch in {0} on {1}'.format(location.name, self.date),
                    description='Autogenerated event',
                    general_area=location,
                    creator=self.creator,
                    is_private=False,
                    status='Proposed'
                )
            appointment.save()
            appointment.invitees.add(*self.people.filter(external_id__in=[p.id for p in g.people]))
            ret.append(appointment)
        return ret

    def generate_appointment_groups(self, location) -> List[LunchAppointmentGroup]:
        """Acts as a bridge between data stored in the data model and the make_groups function"""
        people = self.people.filter(locations=location)
        preexisting_lunch_appointments = self.preexisting_lunch_appointments.filter(general_area=location)

        lunch_people = [
            LunchPerson.factory(p, self.recent_historical_appointments, self.all_historical_appointments)
            for p in people
        ]

        lunch_appointment_groups = [
            LunchAppointmentGroup.factory(g, self.recent_historical_appointments, self.all_historical_appointments)
            for g in preexisting_lunch_appointments
        ]

        finder_bot = FinderBot(lunch_people, lunch_appointment_groups)
        updated_lunch_groups, _ = finder_bot()
        return updated_lunch_groups

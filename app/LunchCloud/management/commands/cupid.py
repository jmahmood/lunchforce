"""
Cupid is responsible for matching together people for lunch.
"""
from argparse import ArgumentParser

from django.core.management.base import BaseCommand

from LunchCloud.helpers import AutoInviteBot


class Command(BaseCommand):
    help = 'Auto-generates lunch meetings for a specific date'

    def add_arguments(self, parser: ArgumentParser):
        # https://docs.python.org/3/library/argparse.html#nargs
        parser.add_argument('date', nargs='+')

    def handle(self, *args, **options):
        for date_str in options['date']:
            invite_bot = AutoInviteBot(date_str)
            results = invite_bot()


from django.db.models.signals import pre_save
from django.dispatch import receiver
from LunchCloud.models import LunchEvents


@receiver(pre_save, sender=LunchEvents)
def event_week_message(sender:LunchEvents, **kwargs):
    # - Send message to Event_(%Week%) for the event being created.
    week_number = sender.event_date.isocalendar()[1]
    pass

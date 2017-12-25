from django.db.models.signals import pre_save
from django.dispatch import receiver
from LunchCloud.models import LunchAppointment


@receiver(pre_save, sender=LunchAppointment)
def event_week_message(sender: LunchAppointment, **kwargs):
    # - Send message to Event_(%Week%) for the event being created.
    week_number = sender.event_date.isocalendar()[1]
    pass

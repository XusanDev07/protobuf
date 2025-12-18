from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.core.models import Application
from apps.core.events.publishers import publish_application_created


@receiver(post_save, sender=Application)
def application_created_signal(sender, instance, created, **kwargs):
    if not created:
        return

    publish_application_created(instance)

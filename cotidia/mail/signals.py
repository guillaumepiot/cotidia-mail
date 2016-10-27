from django.dispatch import receiver
from django.db.models.signals import post_save

from cotidia.mail.models import EmailLog


@receiver(post_save, sender=EmailLog)
def user_update(sender, instance, created, **kwargs):
    pass

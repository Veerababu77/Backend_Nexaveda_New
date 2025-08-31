

from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.core.mail import send_mail

User = get_user_model()

@receiver(post_save, sender = User)
def WelcomeSignal(sender, instance, created, **kwargs):
    """
    When ever new user registered for Nexaveda this signal will send confirmation mail to user.
    """
    if created:
        if instance.email:
            send_mail(
                subject="Welcome to Nexa!",
                message="Thanks for signing up. We’re happy to have you.",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[instance.email],
                fail_silently=False,
            )
        
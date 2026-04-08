import logging

from celery import shared_task
from django.core.mail import send_mail


logger = logging.getLogger(__name__)


@shared_task
def send_system_email(subject: str, body: str, recipient: str) -> None:
    logger.info("Sending email notification to %s", recipient)
    send_mail(subject, body, None, [recipient], fail_silently=True)

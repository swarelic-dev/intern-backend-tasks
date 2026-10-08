import logging
from celery import shared_task

logger = logging.getLogger(__name__)


@shared_task
def send_welcome_sms(phone):
    """
    Asynchronous Celery task that sends a welcome SMS to the contact's phone.
    Mirrors the dispatch_event_async() pattern used in the SCAI rules engine.
    """
    logger.info(f"Sending SMS to {phone}: Welcome to SCAI!")
    return f"Sending SMS to {phone}: Welcome to SCAI!"

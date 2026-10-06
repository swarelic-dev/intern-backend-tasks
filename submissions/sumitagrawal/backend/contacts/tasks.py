from celery import shared_task
import logging

logger = logging.getLogger(__name__)

@shared_task
def send_welcome_sms(phone):
    logger.info(f"Sending SMS to {phone}: Welcome to SCAI!")
    return f"SMS sent to {phone}"

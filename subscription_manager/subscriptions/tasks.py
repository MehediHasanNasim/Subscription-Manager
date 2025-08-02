from celery import shared_task
from django.utils import timezone
from .services.exchange_rate import get_exchange_rate
from .models import ExchangeRateLog
import logging

logger = logging.getLogger(__name__)

@shared_task
def fetch_usd_bdt_rate():
    try:
        rate = get_exchange_rate('USD', 'BDT')
        logger.info(f"Successfully fetched USD-BDT rate: {rate}")
        return rate
    except Exception as e:
        logger.error(f"Failed to fetch USD-BDT rate: {str(e)}")
        raise
import os
from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'subscription_manager.settings')

app = Celery('subscription_manager')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'fetch-usd-bdt-rate-hourly': {
        'task': 'subscriptions.tasks.fetch_usd_bdt_rate',
        'schedule': 3600.0,  # Every hour
    },
}
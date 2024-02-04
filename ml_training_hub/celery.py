# ml_project/celery.py
from __future__ import absolute_import, unicode_literals

import os

from celery import Celery
from celery.schedules import crontab

from ml_training_hub.settings import KAFKA_BOOTSTRAP_SERVERS, KAFKA_TOPIC

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ml_training_hub.settings')
celery_app = Celery('ml_training_hub',
                    broker='confluentkafka://' + KAFKA_BOOTSTRAP_SERVERS + '/' + KAFKA_TOPIC,
                    backend='rpc://',
                    include=['ml_app.tasks'])

celery_app.config_from_object('django.conf:settings', namespace='CELERY')

celery_app.autodiscover_tasks()

celery_app.conf.beat_schedule = {
    'train_ml_model_task': {
        'task': 'ml_app.tasks.train_ml_model_task',
        'schedule': crontab(minute='0', hour='0'),
    }
}

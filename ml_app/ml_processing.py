# ml_app/ml_processing.py
from celery import shared_task

from .kafka_consumer import consume_kafka_messages


@shared_task
def start_kafka_consumer():
    consume_kafka_messages()

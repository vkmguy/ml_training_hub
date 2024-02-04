# tasks.py
from celery import Celery, shared_task
from celery.signals import worker_process_init
from confluent_kafka import Consumer, TopicPartition
from django.conf import settings
from django.core.management import call_command

from ml_app.kafka_consumer import consume_kafka_messages
from ml_app.ml_algorithm import train_ml_algorithm_rf
from ml_app.models import StockData, MLAccuracy
from ml_app.serializers import StockDataSerializer
from ml_training_hub.celery import celery_app


@shared_task
def start_kafka_consumer():
    call_command('kafka_consumer')


@celery_app.task
def train_ml_model_task():
    # Fetch tagged data from the database
    tagged_data = StockData.objects.filter(tag__isnull=False)
    serializer = StockDataSerializer(tagged_data, many=True)

    # Perform ML model training
    accuracy = train_ml_algorithm_rf(serializer.data)
    MLAccuracy.objects.create(accuracy=accuracy)
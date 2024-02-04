# ml_app/management/commands/kafka_consumer.py
from django.core.management.base import BaseCommand
from ml_app.kafka_consumer import consume_kafka_messages


class Command(BaseCommand):
    help = 'Run the Kafka consumer'

    def handle(self, *args, **options):
        consume_kafka_messages()

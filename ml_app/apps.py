from django.apps import AppConfig
from django.core.management import BaseCommand

from ml_app.create_kafka_topic import CreateKafkaTopic


class MlAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ml_app'

    def ready(self):
        from .create_kafka_topic import CreateKafkaTopic
        CreateKafkaTopic().run()


class Command(BaseCommand):
    def handle(self, *args, **options):
        CreateKafkaTopic().run()

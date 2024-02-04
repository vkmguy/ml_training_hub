from django.core.management import BaseCommand

from ml_app.ml_algorithm import train_ml_algorithm_rf
from ml_app.tasks import train_ml_model_task


class Command(BaseCommand):
    help = 'Train the ML Model'

    def handle(self, *args, **options):
        train_ml_model_task()
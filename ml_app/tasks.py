# tasks.py

from ml_app.ml_algorithm import train_ml_algorithm_rf
from ml_app.models import StockData, MLAccuracy
from ml_app.serializers import StockDataSerializer
from ml_training_hub.celery import celery_app


@celery_app.task
def train_ml_model_task():
    # Fetch tagged data from the database
    tagged_data = StockData.objects.filter(tag__isnull=False)
    serializer = StockDataSerializer(tagged_data, many=True)

    # Perform ML model training
    metrics = train_ml_algorithm_rf(serializer.data)
    metrics_to_save = {
        'accuracy': metrics.get('accuracy'),
        'precision': metrics.get('precision'),
        'recall': metrics.get('recall')
    }
    MLAccuracy.objects.create(metrics=metrics_to_save)

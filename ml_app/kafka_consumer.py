# ml_app/kafka_consumer.py
from confluent_kafka import Consumer, KafkaError
from django.conf import settings

from ml_training_hub.settings import KAFKA_TOPIC
from .ml_algorithm import train_ml_algorithm_rf
import json

from .models import MLMetrics, MLAccuracy


def consume_kafka_messages():
    consumer = Consumer({
        'bootstrap.servers': settings.KAFKA_BOOTSTRAP_SERVERS,
        'group.id': 'ml_group',
        'auto.offset.reset': 'earliest'
    })

    topic = KAFKA_TOPIC
    consumer.subscribe([topic])

    try:
        while True:
            msg = consumer.poll(1.0)

            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    continue
                elif msg.error().code() == KafkaError.OFFSET_OUT_OF_RANGE:
                    # Handle offset out of range
                    print('Offset out of range. Seeking to the beginning...')
                    consumer.seek(msg.partition(), 0)
                else:
                    print(msg.error())
                    break

            data = json.loads(msg.value().decode('utf-8'))
            metrics = train_ml_algorithm_rf(data)
            MLAccuracy.objects.create(metrics=metrics)

    except KeyboardInterrupt:
        pass

    finally:
        consumer.close()

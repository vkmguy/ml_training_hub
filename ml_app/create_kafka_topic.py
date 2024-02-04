from confluent_kafka.admin import AdminClient, NewTopic
from django.conf import settings


class CreateKafkaTopic:
    def run(self):
        # Kafka bootstrap servers
        bootstrap_servers = settings.KAFKA_BOOTSTRAP_SERVERS
        # Kafka topic name
        topic_name = settings.KAFKA_TOPIC

        admin_client = AdminClient({'bootstrap.servers': bootstrap_servers})

        topic_metadata = admin_client.list_topics(timeout=5)
        if topic_name not in topic_metadata.topics:
            # Create the topic
            new_topic = NewTopic(topic_name, num_partitions=1, replication_factor=1)
            admin_client.create_topics([new_topic])

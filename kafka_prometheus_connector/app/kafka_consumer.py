import json
from kafka import KafkaConsumer
from kafka.errors import KafkaError
import logging
from app.config import settings
import time

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
)

logger = logging.getLogger(__name__)


def create_kafka_consumer():
    """
    Function to create KafkaConsumer with retry logic.
    This will keep trying to connect to Kafka until successful.
    """
    while True:
        try:
            consumer = KafkaConsumer(
                settings.kafka_topic,  # Topic name from environment
                bootstrap_servers=settings.kafka_bootstrap_servers,  # Kafka broker address from environment
                group_id=settings.kafka_group_id,  # Consumer group id from environment
                auto_offset_reset=settings.kafka_auto_offset_reset,  # Offset reset strategy from environment
            )
            return consumer  # Return consumer instance once it's connected successfully
        except KafkaError as e:
            logger.warning(f"Kafka is not available yet. Retrying in 5 seconds... Error: {e}")
            time.sleep(5)  # Wait before retrying


# Create Kafka Consumer instance with retry logic
consumer = create_kafka_consumer()


def consume_messages():
    """
    Function to consume messages from Kafka and return as JSON.
    """
    for message in consumer:
        # Each message is a JSON string, decode and yield
        yield json.loads(message.value.decode("utf-8"))

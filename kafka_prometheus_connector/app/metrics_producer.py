import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

import json
import random
import time
import logging
from kafka import KafkaProducer
from app.config import settings

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
)

logger = logging.getLogger(__name__)

def create_kafka_producer():
    try:
        producer = KafkaProducer(
            bootstrap_servers=settings.kafka_bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        return producer
    except Exception as e:
        logger.error(f"Error while creating Kafka producer: {e}")
        raise

producer = create_kafka_producer()

def generate_metrics():
    metrics = {
        "Alloc": {
            "Type": "gauge",
            "Name": "Alloc",
            "Description": "Alloc is bytes of allocated heap objects.",
            "Value": random.randint(24000000, 25000000)
        },
        "FreeMemory": {
            "Type": "gauge",
            "Name": "FreeMemory",
            "Description": "RAM available for programs to allocate",
            "Value": random.randint(7500000000, 8000000000)
        },
        "PollCount": {
            "Type": "counter",
            "Name": "PollCount",
            "Description": "PollCount is quantity of metrics collection iteration.",
            "Value": random.randint(1, 5)
        },
        "TotalMemory": {
            "Type": "gauge",
            "Name": "TotalMemory",
            "Description": "Total amount of RAM on this system",
            "Value": random.randint(16000000000, 17000000000)
        }
    }
    return metrics

# Отправка данных в Kafka
def send_metrics_to_kafka():
    while True:
        metrics = generate_metrics()
        try:
            producer.send(settings.kafka_topic, value=metrics)
            logger.info(f"Sent metrics: {metrics}")
        except Exception as e:
            logger.error(f"Error sending message to Kafka: {e}")
        time.sleep(10)  # Ждем 10 секунд перед отправкой новых метрик

# Запуск продюсера
if __name__ == "__main__":
    send_metrics_to_kafka()

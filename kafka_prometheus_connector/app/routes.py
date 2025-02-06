import os
import logging
from fastapi import APIRouter, Response
from app.config import Settings, get_settings
from app.models import KafkaConfig, StatusResponse
from app.prometheus import generate_metrics

router = APIRouter()
settings = get_settings()


def update_env_file(key: str, value: str):
    """Update .env file with new settings"""
    env_vars = {}

    if os.path.exists(".env"):
        with open(".env", "r") as f:
            lines = f.readlines()
            for line in lines:
                k, v = line.strip().split("=", 1)
                env_vars[k] = v

    env_vars[key] = value

    with open(".env", "w") as f:
        for k, v in env_vars.items():
            f.write(f"{k}={v}\n")
            logging.info(f'Setting {k} was updated with {v}')


@router.post("/config", response_model=KafkaConfig)
def set_kafka_config(config: KafkaConfig):
    """
    Set the Kafka topic configuration and persist it in .env.
    """
    update_env_file("KAFKA_TOPIC", config.topic)

    global settings
    settings = get_settings()

    return {"topic": settings.kafka_topic}

@router.get("/status", response_model=StatusResponse)
def get_status():
    """
    Return the current status of the Kafka Connect Emulator.
    """
    return {
        "status": "running",
        "kafka_topic": settings.kafka_topic or "not configured"
    }

@router.get("/metrics")
def get_metrics(response: Response):
    """
    Endpoint to expose metrics in Prometheus format.
    """
    # Generate Prometheus metrics
    metrics = generate_metrics()

    # Return metrics as plain text
    response.headers["Content-Type"] = "text/plain; version=0.0.4; charset=utf-8"

    # Return the first batch of metrics
    rendered_metrics = next(metrics)

    return Response(content=rendered_metrics, media_type="text/plain; charset=utf-8")

@router.get("/health")
async def health():
    return {"status": "ok"}

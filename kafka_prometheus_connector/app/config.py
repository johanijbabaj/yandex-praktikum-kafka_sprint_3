import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    kafka_bootstrap_servers: str = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")
    kafka_topic: str = os.getenv("KAFKA_TOPIC", "metrics_topic")
    kafka_group_id: str = os.getenv("KAFKA_GROUP_ID", "prometheus-consumer")
    kafka_auto_offset_reset: str = os.getenv("KAFKA_AUTO_OFFSET_RESET", "earliest")

    class Config:
        env_file = ".env"  # Load from .env file if available

def get_settings() -> Settings:
    return Settings()

# Create a global settings instance
settings = Settings()

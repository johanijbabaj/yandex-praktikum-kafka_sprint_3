from pydantic import BaseModel

class KafkaConfig(BaseModel):
    topic: str

class StatusResponse(BaseModel):
    status: str
    kafka_topic: str

import json
from kafka import KafkaProducer

from src.settings import settings

producer = KafkaProducer(
    bootstrap_servers=settings.kafka_url,
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)
import json
from kafka import KafkaProducer

producer = KafkaProducer(
    bootstrap_servers="0.0.0.0:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)
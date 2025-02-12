import json
import time
import random
from kafka import KafkaProducer

KAFKA_BROKER = "localhost:9092"
KAFKA_TOPIC = "camera_data"

producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
)

def generate_camera_data():
    """Simulate real-time camera defect detection data."""
    return {
        "machine_id": f"M-{random.randint(1, 10)}",
        "defect_detected": random.choice([True, False]),
        "image_url": f"http://images/{random.randint(1000, 9999)}.jpg",
        "timestamp": int(time.time())
    }

while True:
    data = generate_camera_data()
    producer.send(KAFKA_TOPIC, data)
    print(f"Produced: {data}")
    time.sleep(2)

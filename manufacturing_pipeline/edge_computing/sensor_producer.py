import json
import time
import random
from kafka import KafkaProducer

KAFKA_BROKER = "localhost:9092"
KAFKA_TOPIC = "sensor_data"

producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
)

def generate_sensor_data():
    """Simulate real-time sensor data."""
    return {
        "machine_id": f"M-{random.randint(1, 10)}",
        "temperature": round(random.uniform(50, 100), 2),
        "vibration": round(random.uniform(0, 5), 2),
        "pressure": round(random.uniform(10, 50), 2),
        "timestamp": int(time.time())
    }

while True:
    data = generate_sensor_data()
    producer.send(KAFKA_TOPIC, data)
    print(f"Produced: {data}")
    time.sleep(1)  # Simulating real-time data every second

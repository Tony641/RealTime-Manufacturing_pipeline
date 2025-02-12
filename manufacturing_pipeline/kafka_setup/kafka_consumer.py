import json
import psycopg2
from kafka import KafkaConsumer
from utils.email_alerts import send_email_alert

DATABASE_URL = "dbname=manufacturing user=postgres password=yourpassword host=localhost port=5432"

consumer = KafkaConsumer(
    "anomaly_alerts",
    bootstrap_servers="localhost:9092",
    auto_offset_reset="earliest",
    value_deserializer=lambda v: json.loads(v.decode("utf-8")),
)

conn = psycopg2.connect(DATABASE_URL)
cursor = conn.cursor()

for message in consumer:
    alert = message.value
    cursor.execute("""
        INSERT INTO anomaly_alerts (machine_id, temperature, vibration, pressure, defect_detected, timestamp, alert_message)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (
        alert["machine_id"],
        alert["temperature"],
        alert["vibration"],
        alert["pressure"],
        alert["defect_detected"],
        alert["timestamp"],
        alert["alert_message"]
    ))
    
    conn.commit()
    print(f"Stored Alert: {alert}")

    # Send email alert
    send_email_alert(alert["machine_id"], alert["alert_message"])

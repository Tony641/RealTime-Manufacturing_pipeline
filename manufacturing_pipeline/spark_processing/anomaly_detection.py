from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when, concat_ws
from kafka import KafkaProducer
import json

spark = SparkSession.builder.appName("AnomalyDetection").getOrCreate()

# Load sensor data from PostgreSQL
df_sensor = spark.read.jdbc("jdbc:postgresql://localhost:5432/manufacturing", "sensor_readings")

# Load camera data from PostgreSQL
df_camera = spark.read.jdbc("jdbc:postgresql://localhost:5432/manufacturing", "camera_readings")

# Identify sensor anomalies
df_sensor = df_sensor.withColumn("temperature_anomaly", when(col("temperature") > 80, "High Temperature").otherwise(None))
df_sensor = df_sensor.withColumn("vibration_anomaly", when(col("vibration") > 4, "High Vibration").otherwise(None))
df_sensor = df_sensor.withColumn("pressure_anomaly", when(col("pressure") > 40, "High Pressure").otherwise(None))

# Identify defects from camera data
df_camera = df_camera.withColumn("defect_flag", when(col("defect_detected") == True, "Defect Detected").otherwise(None))

# Merge sensor & camera anomalies
df_anomalies = df_sensor.join(df_camera, "machine_id", "left_outer")

# Concatenate all detected anomalies into a single column
df_anomalies = df_anomalies.withColumn(
    "anomaly_detected",
    concat_ws(", ", col("temperature_anomaly"), col("vibration_anomaly"), col("pressure_anomaly"), col("defect_flag"))
)

# Filter detected anomalies
df_anomalies = df_anomalies.filter(col("anomaly_detected").isNotNull())

# Send anomaly alerts via Kafka
producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
)

for row in df_anomalies.collect():
    alert = {
        "machine_id": row["machine_id"],
        "temperature": row["temperature"],
        "vibration": row["vibration"],
        "pressure": row["pressure"],
        "defect_detected": row["defect_flag"],
        "timestamp": row["timestamp"],
        "anomaly_detected": row["anomaly_detected"],
        "alert_message": f"Anomaly detected: {row['anomaly_detected']}. Immediate attention required!"
    }
    producer.send("anomaly_alerts", alert)
    print(f"Sent alert: {alert}")

from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import subprocess

default_args = {"owner": "airflow", "start_date": datetime(2024, 1, 1)}

dag = DAG("quality_control_pipeline", default_args=default_args, schedule_interval="@daily")

def run_anomaly_detection():
    subprocess.run(["python", "manufacturing_pipeline/spark_processing/anomaly_detection.py"], check=True)

def run_kafka_alert_consumer():
    subprocess.run(["python", "manufacturing_pipeline/kafka_setup/kafka_consumer.py"], check=True)

anomaly_task = PythonOperator(
    task_id="detect_anomalies",
    python_callable=run_anomaly_detection,
    dag=dag,
)

alert_task = PythonOperator(
    task_id="consume_alerts",
    python_callable=run_kafka_alert_consumer,
    dag=dag,
)

anomaly_task >> alert_task

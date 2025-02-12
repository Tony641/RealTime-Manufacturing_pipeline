from fastapi import FastAPI
import psycopg2

app = FastAPI()

DATABASE_URL = "dbname=manufacturing user=postgres password=yourpassword host=localhost port=5432"

def fetch_latest_alerts():
    """Retrieve the latest anomaly alerts from PostgreSQL."""
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM anomaly_alerts ORDER BY timestamp DESC LIMIT 10")
    alerts = cursor.fetchall()
    conn.close()
    return [{"machine_id": a[0], "temperature": a[1], "vibration": a[2], "pressure": a[3], "defect_detected": a[4], "alert_message": a[6]} for a in alerts]

@app.get("/anomalies/")
def get_anomalies():
    """Fetch the latest detected anomalies."""
    return {"alerts": fetch_latest_alerts()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)

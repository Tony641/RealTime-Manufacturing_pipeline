import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

SMTP_SERVER = "smtp.gmail.com"  # Change if using another email provider
SMTP_PORT = 587
EMAIL_SENDER = "your_email@gmail.com"
EMAIL_PASSWORD = "your_app_password"

def send_email_alert(machine_id, alert_message):
    """Sends an email alert for a detected anomaly."""
    recipient = "recipient_email@gmail.com"
    
    subject = f"🚨 Manufacturing Anomaly Detected: {machine_id}"
    body = f"Machine {machine_id} has an anomaly:\n\n{alert_message}\n\nPlease check immediately!"

    msg = MIMEMultipart()
    msg["From"] = EMAIL_SENDER
    msg["To"] = recipient
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_SENDER, recipient, msg.as_string())
        server.quit()
        print(f"📧 Email alert sent to {recipient} for Machine {machine_id}")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")

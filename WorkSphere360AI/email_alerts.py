# email_alerts.py
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

SENDER_EMAIL = "your_email@gmail.com"
SENDER_PASSWORD = "your_app_password"


def send_email(to_email, subject, body):
    msg = MIMEMultipart()
    msg["From"] = SENDER_EMAIL
    msg["To"] = to_email
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain"))

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg)


def send_hr_alerts(dept_alerts):
    for alert in dept_alerts:
        send_email(
            to_email="hr@company.com",
            subject=f" Department Risk Alert: {alert['Department']}",
            body=alert["Alert"]
        )


def send_manager_alerts(df):
    high_risk = df[df["Risk_Level"] == "High"]

    for _, row in high_risk.iterrows():
        send_email(
            to_email="manager@company.com",
            subject=f" High Burnout Risk: Employee {row['Employee_ID']}",
            body=row["AI_Recommendation"]
        )

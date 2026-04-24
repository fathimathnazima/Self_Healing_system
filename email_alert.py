import os
import smtplib
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

load_dotenv()

SENDER_EMAIL=os.getenv("SENDER_EMAIL")
APP_PASSWORD=os.getenv("APP_PASSWORD")
RECEIVER_EMAIL=os.getenv("RECEIVER_EMAIL")


def send_failure_email(service_name, failures, risk):

    subject=f"[ALERT] {service_name} Failure"

    body=f"""
Self-Healing Monitoring Alert

Service: {service_name}
Failures: {failures}
Risk Level: {risk}
Time: {datetime.now()}

Action:
Service automatically restarted.
"""

    try:
        msg=MIMEMultipart()

        msg["From"]=SENDER_EMAIL
        msg["To"]=RECEIVER_EMAIL
        msg["Subject"]=subject

        msg.attach(
            MIMEText(body,"plain")
        )

        server=smtplib.SMTP(
            "smtp.gmail.com",
            587
        )

        server.starttls()

        server.login(
            SENDER_EMAIL,
            APP_PASSWORD
        )

        server.sendmail(
            SENDER_EMAIL,
            RECEIVER_EMAIL,
            msg.as_string()
        )

        server.quit()

        print("Email Alert Sent")

    except Exception as e:
        print(e)
import smtplib
import os
from email.message import EmailMessage
from typing import List
from scraper.logger import setup_logger

logger = setup_logger()

EMAIL_CONFIG = {
    "SMTP_SERVER": "smtp.gmail.com",
    "SMTP_PORT": 587,
    "SENDER_EMAIL": "your_email@gmail.com",
    "SENDER_PASSWORD": "your_app_password",  
    "RECIPIENTS": ["recipient@example.com"],
}


def send_email_with_attachments(subject: str, body: str, attachments: List[str]) -> None:
    try:
        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = EMAIL_CONFIG["SENDER_EMAIL"]
        msg["To"] = ", ".join(EMAIL_CONFIG["RECIPIENTS"])
        msg.set_content(body)

        for filepath in attachments:
            if not os.path.exists(filepath):
                logger.warning(f"Attachment not found: {filepath}")
                continue

            with open(filepath, "rb") as file:
                file_data = file.read()
                file_name = os.path.basename(filepath)
                msg.add_attachment(file_data, maintype="application", subtype="octet-stream", filename=file_name)

        with smtplib.SMTP(EMAIL_CONFIG["SMTP_SERVER"], EMAIL_CONFIG["SMTP_PORT"]) as server:
            server.starttls()
            server.login(EMAIL_CONFIG["SENDER_EMAIL"], EMAIL_CONFIG["SENDER_PASSWORD"])
            server.send_message(msg)
            logger.info("Email with attachments sent successfully.")

    except smtplib.SMTPAuthenticationError as auth_err:
        logger.error(f"[Auth Error] SMTP credentials rejected: {auth_err}")
    except smtplib.SMTPException as smtp_err:
        logger.error(f"[SMTP Error] Email dispatch failed: {smtp_err}")
    except Exception as e:
        logger.error(f"[General Error] Email failed: {e}")

import smtplib
from email.message import EmailMessage
from celery import Celery
from pydantic import EmailStr

from src.settings import settings


celery = Celery("notifications", broker=settings.rabbitmq_url)


class NotificationService:
    @staticmethod
    def create_email_template(
            email_subject: str,
            email_to: str,
            content: str,
            email_from=settings.SMTP_EMAIL_FROM,
    ):
        email = EmailMessage()
        email["Subject"] = email_subject
        email["To"] = email_to
        email["From"] = email_from

        email.set_content(f"<h1>Здравствуйте, {email_to}</h1>\n{content}", subtype="html")
        return email

    @staticmethod
    @celery.task
    def send_email(email_to: EmailStr, email_subject="Test"):
        email = NotificationService.create_email_template(email_to=email_to, email_subject=email_subject, content="Тестовая отправка")
        with smtplib.SMTP_SSL(host=settings.SMTP_HOST, port=settings.SMTP_PORT) as server:
            server.login(user=settings.SMTP_EMAIL_FROM, password=settings.SMTP_PASSWORD)
            server.send_message(email)

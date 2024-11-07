import smtplib

from pydantic import EmailStr
from email.message import EmailMessage

from src.instance import celery
from src.settings import settings


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


# def send_email(sender_email, recipient_email, subject, message, smtp_server, smtp_port, login, password):
#     # Создаем сообщение
#     msg = MIMEMultipart()
#     msg['From'] = sender_email
#     msg['To'] = recipient_email
#     msg['Subject'] = subject
#
#     # Добавляем текст сообщения
#     msg.attach(MIMEText(message, 'plain'))
#
#     try:
#         # Подключаемся к SMTP-серверу
#         with smtplib.SMTP(smtp_server, smtp_port) as server:
#             server.starttls()  # Устанавливаем защищенное соединение
#             server.login(login, password)  # Логинимся на сервере
#             server.sendmail(sender_email, recipient_email, msg.as_string())  # Отправляем письмо
#
#         print("Письмо успешно отправлено!")
#     except Exception as e:
#         print(f"Ошибка при отправке письма: {e}")
#
#
# # Параметры для отправки
# sender_email = "smtptrainme@gmail.com"
# recipient_email = "zorin-ep@mail.ru"
# subject = "Тестовое письмо"
# message = "Привет! Это тестовое письмо, отправленное из Python."
# smtp_server = "smtp.gmail.com"
# smtp_port = 587
# login = "smtptrainme@gmail.com"
# password = "skfd rgdc liuj bkwo "  # Пароль приложения
#
# # Отправка письма
# send_email(sender_email, recipient_email, subject, message, smtp_server, smtp_port, login, password)

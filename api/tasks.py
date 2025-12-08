# api/tasks.py
import logging
from django.core.mail import send_mail
from collect_service.celery import app

log = logging.getLogger(__name__)


@app.task
def send_email_task(subject, message, recipient):
    """Задача отправки email"""
    log.info(
        f"Уведомление по электронной почте пользователю c email:{recipient}"
    )
    send_mail(
        subject=subject,
        message=message,
        from_email='noreply@moneycollect.com',
        recipient_list=[recipient],
        fail_silently=True,
    )

    log.info(f"Отправка на email {recipient}")

    log.info(
        f"Отправка на email {recipient} завершена!",
    )

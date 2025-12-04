# api/tasks.py
from celery import shared_task
from django.core.mail import send_mail


@shared_task
def send_email(subject, message, recipient):
    """Простая задача отправки email"""
    send_mail(
        subject=subject,
        message=message,
        from_email='noreply@moneycollect.com',
        recipient_list=[recipient],
        fail_silently=True,
    )
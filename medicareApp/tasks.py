from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from .models import *

@shared_task
def send_appointment_email(subject, message, email):
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email],
        fail_silently=True
    )
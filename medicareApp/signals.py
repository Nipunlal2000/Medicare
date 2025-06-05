from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Appointment
from .tasks import send_appointment_email

@receiver(post_save, sender=Appointment)
def send_appointment_notification(sender, instance, created, **kwargs):
    if created and hasattr(instance, 'patient') and instance.patient.email:
        
        # Combine date and time for formatting
        formatted_datetime = f"{instance.date.strftime('%d-%m-%Y')} at {instance.time.strftime('%I:%M %p')}"

        message = (
            f"Appointment confirmed\n\n"
            f"Your appointment with Dr. {instance.doctor.user.name} on {formatted_datetime} is confirmed."
        )

        send_appointment_email.apply_async(args=[
            "Appointment Confirmation",
            message,
            instance.patient.email
        ])


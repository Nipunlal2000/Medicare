from django.db import models
from . manager import *
from django.contrib.auth.models import AbstractUser , Group , Permission
from django.utils import timezone

# Create your models here.


class UserProfile(AbstractUser):
 
    username = None
    name = models.CharField(max_length=100,  null=False, default='' )
    email = models.EmailField(unique=True,null=True,blank=True)    
    phone_number = models.CharField(max_length=10, null=True, blank=True)
    is_email_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    otp = models.IntegerField(null=True, blank=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    place = models.CharField(max_length=100, null=True, blank=True)
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('na', 'Not Prefer to Say'),
    ]
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, null=True, blank=True)

    USERNAME_FIELD = 'email'
 
    REQUIRED_FIELDS = []
    groups = models.ManyToManyField(Group, related_name="profile_groups") 
    user_permissions = models.ManyToManyField(Permission, related_name="profile_permissions")
 
    objects = UserManager()
   
    def __str__(self):
        return self.email 
    
# models.py

class Doctors(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='doctor', null=True, blank=True)
    image = models.FileField(upload_to='doctor/', null=True)
    specialization = models.CharField(max_length=100)
    hospital = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    def __str__(self):
            return f"Dr. {self.user.name if self.user else 'Unknown'} - {self.specialization}"

class Appointment(models.Model):
    patient = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='appointments')
    doctor = models.ForeignKey(Doctors, on_delete=models.CASCADE, related_name='appointments')
    date = models.DateField()
    time = models.TimeField()

    class Meta:
        unique_together = ('doctor', 'date', 'time')
    def __str__(self):
            patient_name = self.patient.name if self.patient else "Unknown Patient"
            doctor_name = self.doctor.user.name if self.doctor and self.doctor.user else "Unknown Doctor"
            return f"{patient_name} with Dr. {doctor_name} on {self.date}"


class DoctorAvailability(models.Model):
    REPEAT_CHOICES = [
        ('none', 'No Repeat'),
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('weekdays', 'Weekdays (Mon-Fri)'),
    ]

    doctor = models.ForeignKey('Doctors', on_delete=models.CASCADE, related_name='availability')
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)  # If null, treat as single-day availability
    start_time = models.TimeField()
    end_time = models.TimeField()
    repeat = models.CharField(max_length=20, choices=REPEAT_CHOICES, default='none')

    # Optional: specific weekdays if repeat == 'weekly'
    repeat_days = models.JSONField(null=True, blank=True)  # e.g., ["Monday", "Wednesday"]
    
    def get_repeat_days_display(self):
        if self.repeat == 'weekly' and self.repeat_days:
            return ', '.join(self.repeat_days)
        return ''

    def __str__(self):
        range_str = f"{self.start_date}"
        if self.end_date and self.start_date != self.end_date:
            range_str += f" to {self.end_date}"

        return f"{self.doctor.user.name} available from {range_str}, {self.start_time}–{self.end_time}, repeat: {self.repeat}"




class Records(models.Model):

    # Choices for test type
    TEST_TYPE_CHOICES = [
        ('BLOOD', 'Blood Test'),
        ('XRAY', 'X-Ray'),
        ('MRI', 'MRI Scan'),
        ('CT', 'CT Scan'),
        ('URINE', 'Urine Test'),
        ('OTHER', 'Other'),
    ]

    patient = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    document = models.FileField(upload_to='documents/')
    report = models.CharField(max_length=20, choices=TEST_TYPE_CHOICES)
    description = models.TextField(blank=True, null=True)
    uploaded_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.patient.name} - {self.report}"

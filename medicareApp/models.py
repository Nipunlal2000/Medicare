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
    
class Doctors(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='doctor', null=True, blank=True)
    
    name = models.CharField(max_length=100)
    image = models.FileField(upload_to='doctor/', null=True)
    specialization = models.CharField(max_length=100)
    hospital = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    
    def __str__(self):
        return f"Dr. {self.name} - {self.specialization}"
    
    
class Appointment(models.Model):
    patient = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctors, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()

    class Meta:
        unique_together = ('doctor', 'date', 'time')  # avoid double-booking

    def __str__(self):
        return f"Appointment with {self.doctor.name} on {self.date} at {self.time}"
    
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

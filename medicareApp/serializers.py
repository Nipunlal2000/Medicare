from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
from .models import *
from datetime import date as today_date
from django.db.models import Q
import random

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = UserProfile
        fields = ['name', 'email','age', 'place', 'gender', 'phone_number', 'password', 'confirm_password']

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"confirm_password": "Passwords do not match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = UserProfile.objects.create_user(**validated_data)
        
        return user
    
    
class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(email=data['email'], password=data['password'])
        if not user:
            raise serializers.ValidationError("Invalid email or password.")
        
        if not user.is_email_verified:
            raise serializers.ValidationError("Email not verified. PLease check your email")
        return user
    
    
    
    
class UserSerializer(serializers.ModelSerializer):    
    class Meta:
        model = UserProfile
        fields = ['name','email','password','confirm_password','phone_number','age','place','gender']
        
        
class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()
 
    class Meta:
        fields = ['email']
        
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        exclude = ['password', 'user_permissions', 'groups']

class DoctorListSerializer(serializers.ModelSerializer):
    available_on_date = serializers.SerializerMethodField()
    name = serializers.CharField(source='user.name', read_only=True)

    class Meta:
        model = Doctors
        fields = ['id', 'user','name', 'specialization', 'hospital','image', 'available_on_date']

    def get_available_on_date(self, obj):
        date_str = self.context.get('selected_date')
        if date_str:
            try:
                selected_date = timezone.datetime.strptime(date_str, "%Y-%m-%d").date()
            except ValueError:
                selected_date = timezone.now().date()
        else:
            selected_date = timezone.now().date()

        return obj.availability.filter(start_date__lte=selected_date).filter(
            Q(end_date__gte=selected_date) | Q(end_date__isnull=True)
        ).exists()


class DoctorAvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorAvailability
        fields = ['start_date', 'end_date', 'start_time', 'end_time', 'repeat_days']



class DoctorSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='user.name', read_only=True)

    class Meta:
        model = Doctors
        fields = ['id', 'user', 'name', 'specialization', 'hospital', 'address', 'image']


class AppointmentSerializer(serializers.ModelSerializer):
    doctor_name = serializers.SerializerMethodField(read_only=True)
    patient_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Appointment
        fields = ['id', 'patient', 'doctor', 'date', 'time', 'doctor_name', 'patient_name']

    def get_doctor_name(self, obj):
        return obj.doctor.user.name if obj.doctor and obj.doctor.user else None

    def get_patient_name(self, obj):
        return obj.patient.name if obj.patient else None

def validate(self, data):
    doctor = data.get('doctor')
    patient = data.get('patient') or self.context['request'].user
    date = data.get('date')
    time_slot = data.get('time')

    # 1️⃣ Prevent booking in the past
    if date < today_date.today():
        raise serializers.ValidationError({
            "detail": "You cannot book an appointment in the past."
        })

    # 2️⃣ Prevent same patient booking multiple slots on the same day
    if Appointment.objects.filter(patient=patient, date=date).exists():
        raise serializers.ValidationError({
            "detail": "You already have an appointment on this date."
        })

    # 3️⃣ Prevent booking an already booked time slot with that doctor
    if Appointment.objects.filter(doctor=doctor, date=date, time=time_slot).exists():
        raise serializers.ValidationError({
            "detail": "This time slot is already booked for the selected doctor."
        })

    # 4️⃣ Check if the doctor is available at that date and time
    weekday = date.strftime('%A')
    availabilities = DoctorAvailability.objects.filter(
        doctor=doctor,
        start_date__lte=date
    ).filter(
        models.Q(end_date__gte=date) | models.Q(end_date__isnull=True)
    )

    available = False
    for slot in availabilities:
        if slot.repeat == 'none' and slot.start_date != date:
            continue
        if slot.repeat == 'daily':
            pass
        elif slot.repeat == 'weekdays' and weekday not in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']:
            continue
        elif slot.repeat == 'weekly' and slot.repeat_days and weekday not in slot.repeat_days:
            continue
        elif slot.repeat == 'none' and slot.start_date != date:
            continue

        if slot.start_time <= time_slot < slot.end_time:
            available = True
            break

    if not available:
        raise serializers.ValidationError({
            "detail": "The doctor is not available at this date and time."
        })

    return data

class RecordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Records
        fields = ['id', 'document', 'report', 'description', 'uploaded_at']
        read_only_fields = ['uploaded_at']
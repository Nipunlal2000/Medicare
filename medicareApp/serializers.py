from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
from .models import *
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
        fields = '__all__'
        
        
class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()
 
    class Meta:
        fields = ['email']
        
        
class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = '__all__'

class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ['id', 'patient', 'doctor', 'date', 'time']

    # Optional: Validate if appointment already exists for this doctor at the same date and time
    def validate(self, data):
        if Appointment.objects.filter(doctor=data['doctor'], date=data['date'], time=data['time']).exists():
            raise serializers.ValidationError("This time slot is already booked for the selected doctor.")
        return data

class RecordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Records
        fields = ['id', 'document', 'report', 'description', 'uploaded_at']
        read_only_fields = ['uploaded_at']
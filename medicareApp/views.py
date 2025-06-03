from django.shortcuts import render
from rest_framework.views import APIView,Response
from .serializers import *
# from .tasks import send_otp_email
from django.core.cache import cache
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .mixins import *
from .utils import try_except_wrapper

# Create your views here.



class RegisterView(APIView):
    @try_except_wrapper
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return custom201("Registration successful.", serializer.data)
        return custom400("Registration failed.", serializer.errors)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    @try_except_wrapper
    def post(self, request):
        refresh_token = request.data.get("refresh")
        if refresh_token is None:
            return custom400("Refresh token required.")

        token = RefreshToken(refresh_token)
        token.blacklist()

        return custom200("Logged out successfully.")


class DoctorCreateView(APIView):
    permission_classes = [IsAdminUser]

    @try_except_wrapper
    def post(self, request):
        serializer = DoctorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return custom201("Doctor created successfully.", serializer.data)
        return custom400("Doctor creation failed.", serializer.errors)


class BookAppointmentView(APIView):
    permission_classes = [IsAuthenticated]

    @try_except_wrapper
    def post(self, request):
        data = request.data.copy()
        data['patient'] = request.user.id
        serializer = AppointmentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return custom201("Appointment booked successfully.", serializer.data)
        return custom400("Appointment booking failed.", serializer.errors)


class ReportsUploadView(APIView):
    permission_classes = [IsAuthenticated]

    @try_except_wrapper
    def post(self, request):
        data = request.data.copy()
        data['patient'] = request.user.id

        serializer = RecordsSerializer(data=data)
        if serializer.is_valid():
            serializer.save(patient=request.user)
            return custom201("Report uploaded successfully.", serializer.data)
        return custom400("Report upload failed.", serializer.errors)

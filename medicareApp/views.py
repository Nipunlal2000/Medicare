from django.shortcuts import render
from rest_framework.views import APIView,Response
from .serializers import *
# from .tasks import send_otp_email
from django.core.cache import cache
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .mixins import *
from .utils import try_except_wrapper, flatten_errors
from django.db import IntegrityError

# Create your views here.



class RegisterView(APIView):
    @try_except_wrapper
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return custom201("Registration successful.", serializer.data)
        return custom400("Registration failed.", flatten_errors(serializer.errors))

class LoginView(APIView):

    @try_except_wrapper
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(request, email=email, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            data = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': {
                    'id': user.id,
                    'email': user.email,
                }
            }
            return custom200("Login successful", data)
        else:
            return custom401("Invalid credentials")


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
        return custom400("Doctor creation failed.", flatten_errors(serializer.errors))



class BookAppointmentView(APIView):
    permission_classes = [IsAuthenticated]

    @try_except_wrapper
    def post(self, request):
        data = request.data.copy()
        data['patient'] = request.user.id

        serializer = AppointmentSerializer(data=data)
        if serializer.is_valid():
            try:
                serializer.save()
                return custom201("Appointment booked successfully.", serializer.data)
            except Exception as e:
                return custom400("Appointment save failed.", str(e.__class__.__name__))
        
        return custom400("Appointment booking failed.", flatten_errors(serializer.errors))


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
        return custom400("Report upload failed.", flatten_errors(serializer.errors))

from django.shortcuts import render
from rest_framework.views import APIView,Response
from rest_framework import generics
from .serializers import *
# from .tasks import send_otp_email
from django.core.cache import cache
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .mixins import *
from .utils import try_except_wrapper, flatten_errors
from django.db import IntegrityError
from django.db.models import Q


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




class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)


class DoctorListView(generics.ListAPIView):
    queryset = Doctors.objects.all()
    serializer_class = DoctorListSerializer


class DoctorAvailabilityView(APIView):
    def get(self, request, doctor_id):
        print(f"[DoctorAvailabilityView] doctor_id: {doctor_id}")
        date_str = request.query_params.get('date')
        print(f"[DoctorAvailabilityView] Raw date string: {date_str}")

        if not date_str:
            return Response({"error": "Date is required"}, status=400)

        try:
            date = timezone.datetime.strptime(date_str, '%Y-%m-%d').date()
            print(f"[DoctorAvailabilityView] Parsed date: {date}")
        except ValueError as ve:
            print(f"[DoctorAvailabilityView] Date parsing failed: {ve}")
            return Response({"error": "Invalid date format. Use YYYY-MM-DD"}, status=400)

        try:
            availabilities = DoctorAvailability.objects.filter(
                doctor_id=doctor_id,
                start_date__lte=date
            ).filter(Q(end_date__gte=date) | Q(end_date__isnull=True))

            print(f"[DoctorAvailabilityView] Found {availabilities.count()} availability entries")

            serializer = DoctorAvailabilitySerializer(availabilities, many=True)
            return Response(serializer.data)

        except Exception as e:
            print(f"[DoctorAvailabilityView] Unexpected error: {e}")
            return Response({"error": "Something went wrong", "details": str(e)}, status=500)



class AvailableTimeSlotsView(APIView):
    def get(self, request, doctor_id):
        print(f"[AvailableTimeSlotsView] doctor_id: {doctor_id}")
        date_str = request.query_params.get('date')
        print(f"[AvailableTimeSlotsView] Raw date string: {date_str}")

        if not date_str:
            return Response({"error": "Date is required"}, status=400)

        try:
            date = timezone.datetime.strptime(date_str, '%Y-%m-%d').date()
            print(f"[AvailableTimeSlotsView] Parsed date: {date}")
        except ValueError as ve:
            print(f"[AvailableTimeSlotsView] Date parsing failed: {ve}")
            return Response({"error": "Invalid date format. Use YYYY-MM-DD"}, status=400)

        try:
            availability = DoctorAvailability.objects.filter(
                doctor_id=doctor_id,
                start_date__lte=date
            ).filter(Q(end_date__gte=date) | Q(end_date__isnull=True)).first()

            if not availability:
                print("[AvailableTimeSlotsView] No availability found for this doctor on given date")
                return Response({"message": "Doctor not available on selected date"}, status=404)

            from datetime import timedelta, datetime

            booked_times = Appointment.objects.filter(
                doctor_id=doctor_id,
                date=date
            ).values_list('time', flat=True)

            # print(f"[AvailableTimeSlotsView] Booked times: {list(booked_times)}")

            time_slots = []
            current = datetime.combine(date, availability.start_time)
            end = datetime.combine(date, availability.end_time)

            while current < end:
                time_str = current.time().strftime('%H:%M')
                if current.time() not in booked_times:
                    time_slots.append(time_str)
                current += timedelta(minutes=30)

            # print(f"[AvailableTimeSlotsView] Available slots: {time_slots}")
            return Response({"available_slots": time_slots})

        except Exception as e:
            print(f"[AvailableTimeSlotsView] Unexpected error: {e}")
            return Response({"error": "Something went wrong", "details": str(e)}, status=500)


class AppointmentHistoryView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AppointmentSerializer

    def get_queryset(self):
        return Appointment.objects.filter(patient=self.request.user).order_by('-date')


class CancelAppointmentView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        try:
            appointment = Appointment.objects.get(pk=pk, patient=request.user)
            appointment.delete()
            return Response({'message': 'Appointment cancelled successfully.'})
        except Appointment.DoesNotExist:
            return Response({'error': 'Appointment not found or unauthorized.'}, status=404)

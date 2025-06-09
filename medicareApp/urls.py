from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    path('create-doctor/', DoctorCreateView.as_view(), name='create-doctor'),
    path('book-appointment/', BookAppointmentView.as_view(), name='book-appointment'),
    path('upload-report/', ReportsUploadView.as_view(), name='upload-report'),
    
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('doctors/', DoctorListView.as_view(), name='doctor-list'),
    path('doctor/<int:doctor_id>/availability/', DoctorAvailabilityView.as_view(), name='doctor-availability'),
    path('doctor/<int:doctor_id>/timeslots/', AvailableTimeSlotsView.as_view(), name='available-timeslots'),
    path('appointments/history/', AppointmentHistoryView.as_view(), name='appointment-history'),
    path('appointment/<int:pk>/cancel/', CancelAppointmentView.as_view(), name='cancel-appointment'),

    
]
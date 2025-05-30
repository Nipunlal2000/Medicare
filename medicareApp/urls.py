from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    path('create-doctor/', DoctorCreateView.as_view(), name='create-doctor'),
    path('book-appointment/', BookAppointmentView.as_view(), name='book-appointment'),
    path('upload-report/', ReportsUploadView.as_view(), name='upload-report'),
    
]
from django.urls import path
from .views import *

urlpatterns = [
    path('index', index, name='home'),
    path('', admin_dashboard, name='dashboard'),
    path('login/', admin_login, name='login'),
    path('logout/', admin_logout, name='logout'),
    path('doctor/list/', list_doctor, name='list_doctor'),
    path('doctor/create/', create_doctor, name='create_doctor'),
    path('doctor/update/<int:pk>/', update_doctor, name='update_doctor'),
    path('doctor/detail/<int:pk>/', detail_doctor, name='detail_doctor'),
    path('doctor/delete/<int:pk>/', delete_doctor, name='delete_doctor'),
    # path('doctor/<int:doctor_id>/availability/', doctor_availability, name='doctor_availability'),
    # path('doctor/<int:doctor_id>/book/', book_appointment, name='book_appointment'),
]
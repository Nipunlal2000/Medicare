from django.contrib import admin
from .models import UserProfile, Doctor, Appointment, Records

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone_number')

class DoctorAdmin(admin.ModelAdmin):
    list_display = ('name', 'specialization', 'hospital')
    search_fields = ('name', 'specialization', 'hospital')
    list_filter = ('specialization',)

class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'date', 'time')
    search_fields = ('doctor__name', 'patient__email')
    list_filter = ('date', 'doctor')

class RecordsAdmin(admin.ModelAdmin):
    list_display = ('patient', 'report', 'uploaded_at')
    list_filter = ('report', 'uploaded_at')
    search_fields = ('patient__email', 'description')

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Doctor, DoctorAdmin)
admin.site.register(Appointment, AppointmentAdmin)
admin.site.register(Records, RecordsAdmin)

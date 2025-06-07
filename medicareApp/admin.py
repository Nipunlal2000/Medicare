from django.contrib import admin
from .models import *

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone_number')

class DoctorAdmin(admin.ModelAdmin):
    list_display = ('get_name', 'specialization', 'hospital')
    search_fields = ('user__name', 'specialization', 'hospital')
    list_filter = ('specialization',)

    def get_name(self, obj):
        return obj.user.name if obj.user else '-'
    get_name.short_description = 'Name'

class DoctorAvailabilityAdmin(admin.ModelAdmin):
    list_display = (
        'doctor_name',
        'start_date',
        'end_date',
        'start_time',
        'end_time',
        'repeat',
        'get_repeat_days',
    )
    list_filter = ('repeat', 'start_date')
    search_fields = ('doctor__user__name',)
    ordering = ('-start_date',)

    def doctor_name(self, obj):
        return obj.doctor.user.name if obj.doctor and obj.doctor.user else "-"
    doctor_name.short_description = "Doctor"

    def get_repeat_days(self, obj):
        return ', '.join(obj.repeat_days) if obj.repeat == 'weekly' and obj.repeat_days else '-'
    get_repeat_days.short_description = "Repeat Days"

class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'date', 'time')
    search_fields = ('doctor__name', 'patient__email')
    list_filter = ('date', 'doctor')

class RecordsAdmin(admin.ModelAdmin):
    list_display = ('patient', 'report', 'uploaded_at')
    list_filter = ('report', 'uploaded_at')
    search_fields = ('patient__email', 'description')

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Doctors, DoctorAdmin)
admin.site.register(Appointment, AppointmentAdmin)
admin.site.register(Records, RecordsAdmin)
admin.site.register(DoctorAvailability, DoctorAvailabilityAdmin)

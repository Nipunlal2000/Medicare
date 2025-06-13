from django.shortcuts import render,redirect, get_object_or_404
from medicareApp.models import *
from .forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.db.models import Q
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.conf import settings
from axes.models import AccessAttempt

def index(request):
    return render(request,'index.html')

def admin_login(request):
    error = None
    cooldown_minutes = settings.AXES_COOLOFF_TIME or 5
    failure_limit = settings.AXES_FAILURE_LIMIT or 3

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Get latest attempt
        attempt = AccessAttempt.objects.filter(username=email).order_by('-attempt_time').first()
        failures = 0

        if attempt:
            if cooldown_minutes:
                locked_until = attempt.attempt_time + timezone.timedelta(minutes=cooldown_minutes)
                if timezone.now() > locked_until:
                    attempt.delete()  # 🔁 Cooldown expired, reset
                else:
                    failures = attempt.failures_since_start
            else:
                failures = attempt.failures_since_start

        # 🔐 Lockout message
        if failures >= failure_limit:
            minutes_left = 0
            locked_until = attempt.attempt_time + timezone.timedelta(minutes=cooldown_minutes)
            seconds_remaining = (locked_until - timezone.now()).total_seconds()
            if seconds_remaining > 0:
                minutes_left = int(seconds_remaining // 60) or 1
            error = f"Too many failed attempts. Try again after {minutes_left} minute(s)."
            return render(request, 'admin_login.html', {'error': error})

        # 🧠 Authenticate
        user = authenticate(request, email=email, password=password)

        if user is not None and user.is_staff:
            login(request, user)
            return redirect('dashboard')
        else:
            remaining_attempts = max(failure_limit - failures - 1, 0)
            error = f"Invalid email or password. {remaining_attempts} attempt(s) left."

    return render(request, 'admin_login.html', {'error': error})

@login_required(login_url='admin_login')
def admin_dashboard(request):
    query = request.GET.get('q', '').strip()
    
    doctors_list = Doctors.objects.all()

    if query:
        # Create separate queries for different match types
        starts_with = (
            Q(user__name__istartswith=query) |
            Q(specialization__istartswith=query) |
            Q(hospital__istartswith=query)
        )
        
        contains = (
            Q(user__name__icontains=query) |
            Q(specialization__icontains=query) |
            Q(hospital__icontains=query)
        ) & ~starts_with  # Exclude items that already match starts_with

        # Combine with priority to starts_with matches
        doctors_list = doctors_list.filter(starts_with | contains).annotate(
            match_priority=models.Case(
                models.When(starts_with, then=1),
                models.When(contains, then=2),
                default=3,
                output_field=models.IntegerField()
            )
        ).order_by('match_priority', 'user__name')
    
    total_doctors = doctors_list.count()
    doctor_user_ids = Doctors.objects.values_list('user_id', flat=True)

    regular_users = UserProfile.objects.filter(
        is_superuser=False,
    ).exclude(id__in=doctor_user_ids)

    total_regular_users = regular_users.count()
    
    total_patients_with_appointments = Appointment.objects.values('patient').distinct().count()
    
    paginator = Paginator(doctors_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'admin_dashboard.html', {
        'page_obj': page_obj,
        'query': query,
        'total_doctors': total_doctors,
        'total_regular_users': total_regular_users,
        'total_patients_with_appointments': total_patients_with_appointments 
    })

def admin_logout(request):
    logout(request)
    return redirect('login')


@login_required(login_url='admin_login')
def list_doctor(request):
    query = request.GET.get('q', '').strip()
    
    doctors_list = Doctors.objects.all().order_by('user__name')

    if query:
        # Create separate queries for different match types
        starts_with = (
            Q(user__name__istartswith=query) |
            Q(specialization__istartswith=query) |
            Q(hospital__istartswith=query)
        )
        
        contains = (
            Q(user__name__icontains=query) |
            Q(specialization__icontains=query) |
            Q(hospital__icontains=query)
        ) & ~starts_with  # Exclude items that already match starts_with

        # Combine with priority to starts_with matches
        doctors_list = doctors_list.filter(starts_with | contains).annotate(
            match_priority=models.Case(
                models.When(starts_with, then=1),
                models.When(contains, then=2),
                default=3,
                output_field=models.IntegerField()
            )
        ).order_by('match_priority', 'user__name')
    
    paginator = Paginator(doctors_list, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'list_doctors.html', {
        'page_obj': page_obj,
        'query': query,
    })
    

@login_required(login_url='admin_login')
def list_patients(request):
    query = request.GET.get('q', '').strip()
    
    # Exclude superusers and doctor-linked users
    doctor_user_ids = Doctors.objects.exclude(user=None).values_list('user_id', flat=True)
    patients = UserProfile.objects.filter(is_superuser=False).exclude(id__in=doctor_user_ids)

    if query:
        starts_with = (
            Q(name__istartswith=query) |
            Q(email__istartswith=query) |
            Q(phone_number__istartswith=query) |
            Q(place__istartswith=query)
        )
        contains = (
            Q(name__icontains=query) |
            Q(email__icontains=query) |
            Q(phone_number__icontains=query) |
            Q(place__icontains=query)
        ) & ~starts_with

        patients = patients.filter(starts_with | contains).annotate(
            match_priority=models.Case(
                models.When(starts_with, then=1),
                models.When(contains, then=2),
                default=3,
                output_field=models.IntegerField()
            )
        ).order_by('match_priority', 'name')

    # Pagination
    paginator = Paginator(patients, 10)  # 6 per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'list_patients.html', {
        'page_obj': page_obj,
        'query': query,
    })
    

@login_required(login_url='admin_login')
def list_appointment(request):
    query = request.GET.get('q', '').strip()

    appointments = Appointment.objects.select_related('patient', 'doctor', 'doctor__user')

    if query:
        appointments = appointments.filter(
            Q(patient__name__icontains=query) |
            Q(doctor__user__name__icontains=query) |
            Q(date__icontains=query)
        )

    appointments = appointments.order_by('-date', '-time')

    paginator = Paginator(appointments, 10)  # 10 appointments per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'appointments.html', {
        'page_obj': page_obj,
        'query': query,
    })
   

@login_required(login_url='admin_login')
def create_doctor(request):
    if request.method == "POST":
        form = DoctorForm(request.POST, request.FILES)
        email = request.POST.get('email')
        password = request.POST.get('password')
        name = request.POST.get('name')  # This is the name for UserProfile

        if form.is_valid() and email and password and name:
            # Create the user
            user = UserProfile.objects.create_user(
                email=email,
                password=password,
                name=name
            )

            # Create the doctor and link the user
            doctor = form.save(commit=False)
            doctor.user = user
            doctor.save()
            return redirect('dashboard')
    else:
        form = DoctorForm()

    return render(request, 'create_doctor.html', {'form': form})



def detail_doctor(request, pk):
    doctor = get_object_or_404(Doctors, pk=pk)
    return render(request, 'detail_doctor.html', {'doctor': doctor})


def update_doctor(request, pk):
    doctor = get_object_or_404(Doctors, pk=pk)
    user = doctor.user  # Access related UserProfile

    if request.method == 'POST':
        form = DoctorForm(request.POST, request.FILES, instance=doctor)
        name = request.POST.get('name')

        if form.is_valid() and name:
            form.save()
            user.name = name  # update name from POST data
            user.save()
            return redirect('dashboard')
    else:
        form = DoctorForm(instance=doctor)
    
    context =  {
        'form': form,
        'edit': True,
        'doctor': doctor,
        'doctor_name': user.name  
    }
    return render(request, 'update_doctor.html',context)


def delete_doctor(request, pk):
    doctor = get_object_or_404(Doctors, pk=pk)
    if request.method == 'POST':
        doctor.delete()
        return redirect('dashboard')
    return redirect('dashboard')


def doctor_login(request):
    error = None
    cooldown_minutes = settings.AXES_COOLOFF_TIME or 5
    failure_limit = settings.AXES_FAILURE_LIMIT or 3

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Fetch last attempt
        attempt = AccessAttempt.objects.filter(username=email).order_by('-attempt_time').first()
        failures = 0

        if attempt:
            cooldown = settings.AXES_COOLOFF_TIME
            if cooldown:
                locked_until = attempt.attempt_time + timezone.timedelta(minutes=cooldown)
                if timezone.now() > locked_until:
                    attempt.delete()  # 🔁 Reset after cooldown
                else:
                    failures = attempt.failures_since_start
            else:
                failures = attempt.failures_since_start

        # Check lockout
        if failures >= failure_limit:
            minutes_left = 0
            if cooldown_minutes:
                locked_until = attempt.attempt_time + timezone.timedelta(minutes=cooldown_minutes)
                seconds_remaining = (locked_until - timezone.now()).total_seconds()
                if seconds_remaining > 0:
                    minutes_left = int(seconds_remaining // 60) or 1
            error = f"Too many failed attempts. Try again after {minutes_left} minute(s)."
            return render(request, 'doctor_login.html', {'error': error})

        # Attempt authentication
        user = authenticate(request, email=email, password=password)

        if user is not None and not user.is_staff:
            login(request, user)
            return redirect('/doctor/')
        else:
            remaining_attempts = max(failure_limit - failures - 1, 0)
            error = f"Invalid email or password. {remaining_attempts} attempt(s) left."

    return render(request, 'doctor_login.html', {'error': error})




@login_required(login_url='doctor_login')
def doctor_dashboard(request):
    # Get the doctor object for the logged-in user
    doctor = get_object_or_404(Doctors, user=request.user)

    # Get distinct patients who booked with this doctor
    patients = UserProfile.objects.filter(
        appointments__doctor=doctor
    ).distinct()

    appointments = Appointment.objects.filter(doctor=doctor).select_related('patient')
    return render(request, 'doctor_dashboard.html', {
        'doctor': doctor,
        'patients': patients,
        'appointments': appointments
    })


@login_required(login_url='doctor_login')
def booked_appointments(request):
    # Get the logged-in doctor
    doctor = get_object_or_404(Doctors, user=request.user)

    # Fetch appointments for this doctor, most recent first
    appointments = Appointment.objects.select_related('patient').filter(
        doctor=doctor
    ).order_by('-date', '-time')

    return render(request, 'booked_appointments.html', {
        'appointments': appointments,
        'doctor': doctor,
    })




@login_required(login_url='doctor_login')
def doctor_availability_view(request):
    
    if not hasattr(request.user, 'doctor'):
        raise PermissionDenied("Only doctors can access this page.")

    doctor = request.user.doctor
    availabilities = DoctorAvailability.objects.filter(doctor=doctor).order_by('start_date', 'start_time')

    if request.method == 'POST':
        form = AvailabilityForm(request.POST)
        if form.is_valid():
            availability = form.save(commit=False)
            availability.doctor = doctor
            availability.save()
            form.save_m2m()  # ✅ This saves the repeat_days many-to-many or list
            return redirect('doctor_availability')
    else:
        form = AvailabilityForm()

    day_list = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    
    context = {
        'form': form,
        'availabilities': availabilities,
        'day_list': day_list,
        'doctor' : doctor
    }
    
    return render(request, 'doctor_availability.html', context)

@login_required(login_url='doctor_login')
def edit_availability_view(request, pk):
    if not hasattr(request.user, 'doctor'):
        raise PermissionDenied("Only doctors can access this page.")
    
    doctor = request.user.doctor
    availability = get_object_or_404(DoctorAvailability, pk=pk, doctor=doctor)

    if request.method == 'POST':
        form = AvailabilityForm(request.POST, instance=availability)
        if form.is_valid():
            form.save()
            return redirect('doctor_availability')
    else:
        form = AvailabilityForm(instance=availability)

    return render(request, 'doctor_edit_availability.html', {'form': form,'doctor' : doctor})


@login_required(login_url='doctor_login')
@require_POST
def delete_availability_view(request, pk):
    if not hasattr(request.user, 'doctor'):
        raise PermissionDenied("Only doctors can access this page.")

    doctor = request.user.doctor
    availability = get_object_or_404(DoctorAvailability, pk=pk, doctor=doctor)
    availability.delete()
    return redirect('doctor_availability')

@login_required(login_url='doctor_login')
def doctor_profile(request):
    if not hasattr(request.user, 'doctor'):
        raise PermissionDenied("Only doctors can access this page.")

    doctor = request.user.doctor
    return render(request, 'doctor_profile.html', {'doctor': doctor})


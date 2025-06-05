from django.shortcuts import render,redirect, get_object_or_404
from medicareApp.models import *
from .forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied


def index(request):
    return render(request,'index.html')

def admin_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None and user.is_staff:
            login(request, user)
            return redirect('/')
        else:
            messages.error(request, "Invalid credentials or not an admin user")
    return render(request, 'admin_login.html')

@login_required(login_url='admin_login')
def admin_dashboard(request):
    doctors = Doctors.objects.all()
    return render(request, 'admin_dashboard.html',{'doctors':doctors,})

def admin_logout(request):
    logout(request)
    return redirect('login')


@login_required(login_url='admin_login')
def list_doctor(request):
    doctors = Doctors.objects.all()
    return render(request, 'list_doctors.html',{'doctors':doctors})

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
            return redirect('/')
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
            return redirect('/')
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
        return redirect('/')
    return redirect('/')




def doctor_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None and not user.is_staff:
            login(request, user)
            return redirect('/doctor/')
        else:
            messages.error(request, "Invalid credentials or not an doctor user")
    return render(request, 'doctor_login.html')


@login_required(login_url='doctor_login')
def doctor_dashboard(request):
    doctor = get_object_or_404(Doctors, user__email=request.user.email)
    patients = UserProfile.objects.filter(appointments__doctor=doctor).distinct()
    
    return render(request, 'doctor_dashboard.html',{'doctor': doctor, 'patients':patients})


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
def doctor_profile(request):
    if not hasattr(request.user, 'doctor'):
        raise PermissionDenied("Only doctors can access this page.")

    doctor = request.user.doctor
    return render(request, 'doctor_profile.html', {'doctor': doctor})

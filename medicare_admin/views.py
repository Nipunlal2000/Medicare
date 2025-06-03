from django.shortcuts import render,redirect, get_object_or_404
from medicareApp.models import *
from .forms import DoctorForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

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
    return render(request, 'admin_dashboard.html',{'doctors':doctors})

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
        email = request.POST.get('email')  # or from a separate form
        password = request.POST.get('password')
        
        if form.is_valid() and email and password:
            # Create user first
            user = UserProfile.objects.create_user(email=email, password=password)
            
            # Save doctor with user linked
            doctor = form.save(commit=False)
            doctor.user = user  # assign the newly created user
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
    if request.method == 'POST':
        form = DoctorForm(request.POST, request.FILES, instance=doctor)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = DoctorForm(instance=doctor)
    return render(request, 'update_doctor.html', {'form': form, 'edit': True, 'doctor': doctor})


def delete_doctor(request, pk):
    doctor = get_object_or_404(Doctors, pk=pk)
    if request.method == 'POST':
        doctor.delete()
        return redirect('/')
    return redirect('/')





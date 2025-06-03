# adminpanel/forms.py
from django import forms
from medicareApp.models import Doctors

class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctors
        fields = ['name','image', 'specialization', 'hospital', 'address']



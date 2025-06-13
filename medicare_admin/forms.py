# adminpanel/forms.py
from django import forms
from medicareApp.models import *

class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctors
        fields = ['image', 'specialization', 'hospital', 'address']


class AvailabilityForm(forms.ModelForm):
    repeat_days = forms.MultipleChoiceField(
        choices=[
            ('Monday', 'Monday'),
            ('Tuesday', 'Tuesday'),
            ('Wednesday', 'Wednesday'),
            ('Thursday', 'Thursday'),
            ('Friday', 'Friday'),
            ('Saturday', 'Saturday'),
            ('Sunday', 'Sunday'),
        ],
        widget=forms.CheckboxSelectMultiple,
        required=True  # ✅ Must select at least one day
    )

    class Meta:
        model = DoctorAvailability
        fields = ['start_date', 'end_date', 'start_time', 'end_time', 'repeat_days']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get("start_time")
        end_time = cleaned_data.get("end_time")
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")
        repeat_days = cleaned_data.get("repeat_days")

        # 1️⃣ Time validation
        if start_time and end_time and start_time >= end_time:
            raise forms.ValidationError("End time must be after start time.")

        # 2️⃣ Date range validation
        if start_date and end_date and start_date > end_date:
            raise forms.ValidationError("End date cannot be before start date.")

        # 3️⃣ Repeat days validation
        if not repeat_days:
            raise forms.ValidationError("Please select at least one repeat day.")

        return cleaned_data

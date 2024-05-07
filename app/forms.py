from django import forms # Import the forms module from Django for the forms to work
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm # Import the forms needed for the login and registration forms to work
from django.contrib.auth.models import User # Import the User model for the forms to work
from .models import Pet, Appointment, MedicalRecord, VaccinationRecord # Import the models for the forms to work
import datetime # for datetime-local input to work
from django.core.exceptions import ValidationError # for custom validation to work
from .models import Profile # Import the Profile model for the forms to work


class RegisterForm(UserCreationForm): # Form for registering new users
    email = forms.EmailField() # Email input

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"] # Fields to include in the form

class LoginForm(AuthenticationForm): # Form for logging in
    username = forms.CharField() # Username input
    password = forms.CharField(widget=forms.PasswordInput) # Password input

def generate_time_choices():
    times = []
    start = datetime.time(hour=8, minute=0)
    end = datetime.time(hour=18, minute=0)
    time_delta = datetime.timedelta(minutes=30)  # Assuming appointments every 30 minutes

    current_time = start
    while current_time <= end:
        formatted_time = current_time.strftime('%H:%M')
        times.append((formatted_time, formatted_time))
        current_time = (datetime.datetime.combine(datetime.date.today(), current_time) + time_delta).time()

    # Adjust end time for Saturday
    saturday_end = datetime.time(hour=15, minute=0)
    saturday_times = []
    current_time = start
    while current_time <= saturday_end:
        formatted_time = current_time.strftime('%H:%M')
        saturday_times.append((formatted_time, formatted_time))
        current_time = (datetime.datetime.combine(datetime.date.today(), current_time) + time_delta).time()

    return times, saturday_times


TIME_CHOICES, SATURDAY_TIME_CHOICES = generate_time_choices()

class AppointmentForm(forms.ModelForm):
    date = forms.DateField(widget=forms.SelectDateWidget)
    time = forms.ChoiceField(choices=TIME_CHOICES)  # Updated with generated time choices

    class Meta:
        model = Appointment
        fields = ['pet', 'date', 'time', 'appointment_type', 'notes']
        widgets = {
            'notes': forms.Textarea(),
        }

    def clean_date(self):
        date = self.cleaned_data['date']
        if date.weekday() == 6:  # Sunday is 6
            raise ValidationError("The clinic is closed on Sundays.")
        if date.weekday() == 5:  # Saturday
            self.fields['time'].choices = SATURDAY_TIME_CHOICES  # Adjust time choices for Saturdays
        else:
            self.fields['time'].choices = TIME_CHOICES  # Reset to normal hours if the date changes
        return date

    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get('date')
        time = cleaned_data.get('time')
        if date and time:
            appointment_time = datetime.datetime.strptime(time, '%H:%M').time()
            if (date.weekday() == 5 and appointment_time > datetime.time(hour=15, minute=0)) or (date.weekday() < 5 and appointment_time > datetime.time(hour=18, minute=0)):
                raise ValidationError("Selected time is outside of operating hours.")
        return cleaned_data

class PetForm(forms.ModelForm): # Form for creating pets
    class Meta:
        model = Pet
        fields = ['name', 'breed', 'age', 'weight', 'color'] # Fields to include in the form

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'breed': forms.TextInput(attrs={'class': 'form-control'}),
            'age': forms.NumberInput(attrs={'class': 'form-control'}),
            'weight': forms.NumberInput(attrs={'class': 'form-control'}),
            'color': forms.TextInput(attrs={'class': 'form-control'}),
        }

class PhotoUploadForm(forms.ModelForm): # Form for uploading pet photos
    class Meta:
        model = Pet
        fields = ['photo'] # Only include the photo field in the form

# address form for edit profile
class AddressForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['address'] # Only include the address field in the form

# phone form for edit profile
class PhoneForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone'] # Only include the phone field in the form

# email form for edit profile
class EmailForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email'] # Only include the email field in the form

# change password form for edit profile
class ChangePasswordForm(PasswordChangeForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(user, *args, **kwargs)
        self.fields['new_password1'].widget = forms.PasswordInput(attrs={'class': 'form-control'})
        self.fields['new_password2'].widget = forms.PasswordInput(attrs={'class': 'form-control'})

class MedicalRecordForm(forms.ModelForm):
    class Meta:
        model = MedicalRecord
        fields = ['document'] # Only include the document field in the form

class VaccinationRecordForm(forms.ModelForm):
    class Meta:
        model = MedicalRecord
        fields = ['document'] # Only include the document field in the form
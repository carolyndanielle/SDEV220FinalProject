from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Pet


class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

class LoginForm(AuthenticationForm):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class AppointmentForm(forms.Form):
    date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        help_text="Select a date for the appointment."
    )
    time = forms.TimeField(
        widget=forms.TimeInput(attrs={'type': 'time'}),
        help_text="Select a time for the appointment."
    )

class PetForm(forms.ModelForm):
    class Meta:
        model = Pet
        fields = ['name', 'breed', 'age', 'weight']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'breed': forms.TextInput(attrs={'class': 'form-control'}),
            'age': forms.NumberInput(attrs={'class': 'form-control'}),
            'weight': forms.NumberInput(attrs={'class': 'form-control'}),
        }

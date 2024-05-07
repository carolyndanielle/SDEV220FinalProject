from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import AppointmentForm, PetForm, PhotoUploadForm, EmailForm, AddressForm, PhoneForm, MedicalRecordForm, VaccinationRecordForm
from .models import Pet, VaccinationRecord, Profile, MedicalRecord, Appointment
from django.http import HttpResponse
from datetime import datetime, time
from django.views.decorators.http import require_POST

# Registration view
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful. Welcome to your dashboard!')
            return redirect('dashboard')
        else:
            for field, error_list in form.errors.items():
                for error in error_list:
                    messages.error(request, f"{field}: {error}")
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

# Login view
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Successfully logged in.')
                return redirect('dashboard')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

# Logout view
def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('login')  # Redirect to login page after logout

# Dashboard view
@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

@login_required
def settings_view(request):
    # Your settings logic here
    return render(request, 'settings.html')

# User profile view
@login_required
def user_profile(request):
    profile = request.user.profile
    return render(request, 'profile.html', {'profile': profile})

# Edit profile view
@login_required
def edit_profile(request):
    # Your view logic here
    return render(request, 'edit_profile.html')

# Delete profile view
@login_required
def delete_profile(request):
    # Your view logic here
    return render(request, 'delete_profile.html')

@login_required
def book_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            try:
                appointment = form.save(commit=False)
                date = form.cleaned_data['date']
                time_str = form.cleaned_data['time']
                # Convert the time string to a time object
                appointment_time = datetime.strptime(time_str, '%H:%M').time()
                # Combine date and time to create a datetime object
                appointment_date_time = datetime.combine(date, appointment_time)
                appointment.date_time = appointment_date_time
                appointment.pet = Pet.objects.first()  # Example: Assigning a pet for the appointment
                appointment.save()
                messages.success(request, "Your appointment has been booked successfully.")
                return redirect('appointment_confirmation')
            except Exception as e:
                messages.error(request, f"Error booking appointment: {str(e)}")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = AppointmentForm()
    return render(request, 'book_appointment.html', {'form': form})

# Manage pets view
@login_required
def manage_pets(request):
    pets = Pet.objects.filter(owner=request.user)
    return render(request, 'manage_pets.html', {'pets': pets})

@login_required
def pet_detail(request, pet_id):
    pet = get_object_or_404(Pet, pk=pet_id)
    return render(request, 'pet_detail.html', {'pet': pet})


# View appointments view
@login_required
def appointments_view(request):
    # Filter appointments where the pet's owner is the current user
    appointments = Appointment.objects.filter(pet__owner=request.user).order_by('-date_time')
    return render(request, 'appointments.html', {'appointments': appointments})

@login_required
def appointment_details(request, id):
    appointment = get_object_or_404(Appointment, pk=id)
    return render(request, 'appointment_details.html', {'appointment': appointment})

# Vaccination records view
@login_required
def vaccination_records(request):
    records = VaccinationRecord.objects.filter(pet__owner=request.user).order_by('-uploaded_date')
    return render(request, 'vaccination_records.html', {'records': records})

# Medical records view
@login_required
def medical_records(request):
    records = MedicalRecord.objects.filter(pet__owner=request.user)
    return render(request, 'medical_records.html', {'records': records})

# Add pet view
@login_required
def add_pet(request):
    if request.method == 'POST':
        form = PetForm(request.POST)
        if form.is_valid():
            pet = form.save(commit=False)
            pet.owner = request.user # Ensure you are associating the pet with the user
            pet.save()
            return redirect('manage_pets')
    else:
        form = PetForm()
    return render(request, 'add_pet.html', {'form': form})

# upload photo view
def upload_photo(request, pet_id):
    pet = Pet.objects.get(id=pet_id)
    if request.method == 'POST':
        form = PhotoUploadForm(request.POST, request.FILES, instance=pet)
        if form.is_valid():
            form.save()
            return redirect('pet_detail', pet_id=pet.id)
    else:
        form = PhotoUploadForm(instance=pet)
    return render(request, 'upload_photo.html', {'form': form, 'pet': pet})

# Edit email view
@login_required
def edit_email(request):
    if request.method == 'POST':
        form = EmailForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Email successfully updated.')
            return redirect('edit_profile')
    else:
        form = EmailForm(instance=request.user)
    return render(request, 'edit_email.html', {'form': form})

# Edit address view
@login_required
def edit_address(request):
    if request.method == 'POST':
        form = AddressForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Address successfully updated.')
            return redirect('edit_profile')
    else:
        form = AddressForm(instance=request.user.profile)
    return render(request, 'edit_address.html', {'form': form})

# Edit phone number view
@login_required
def edit_phone_number(request):
    if request.method == 'POST':
        form = PhoneForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Phone number successfully updated.')
            return redirect('edit_profile')
    else:
        form = PhoneForm(instance=request.user.profile)
    return render(request, 'edit_phone.html', {'form': form})

# Change password view
@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important to maintain the user's session
            messages.success(request, 'Your password was successfully updated!')
            return redirect('edit_profile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {'form': form})

@login_required
def edit_appointment(request, id):
    appointment = get_object_or_404(Appointment, pk=id)
    if request.method == 'POST':
        form = AppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            date = form.cleaned_data['date']
            time_str = form.cleaned_data['time']
            time_obj = datetime.strptime(time_str, '%H:%M').time()  # Converts time string to time object
            appointment.date_time = datetime.combine(date, time_obj)
            appointment.save()
            messages.success(request, "Appointment rescheduled successfully.")
            return redirect('appointments_view')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = AppointmentForm(instance=appointment)
    return render(request, 'edit_appointment.html', {'form': form})


@login_required
def cancel_appointment(request, id):
    appointment = get_object_or_404(Appointment, pk=id)
    if request.method == 'POST':
        appointment.status = 'cancelled'
        appointment.save()
        messages.success(request, "Appointment cancelled successfully.")
        return redirect('appointments_view')
    else:
        # Handle GET request properly, maybe redirect to appointments_view or show an error message
        return redirect('appointments_view')

def upload_medical_record(request):
    if request.method == 'POST':
        form = MedicalRecordForm(request.POST, request.FILES)
        if form.is_valid():
            medical_record = form.save(commit=False)
            medical_record.user = request.user
            medical_record.save()
            return redirect('profile')  # Redirect to user's profile page
    else:
        form = MedicalRecordForm()
    return render(request, 'medical_record_upload.html', {'form': form})

# upload vaccination record
def upload_vaccination_record(request):
    if request.method == 'POST':
        form = VaccinationRecordForm(request.POST, request.FILES)
        if form.is_valid():
            vaccination_record = form.save(commit=False)
            vaccination_record.save()
            messages.success(request, 'Vaccination record uploaded successfully.')
            return redirect('vaccination_records')  # Redirect to the vaccination records page
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = VaccinationRecordForm()
    return render(request, 'upload_vaccination_record.html', {'form': form})

# Appointment confirmation view
@login_required
def appointment_confirmation(request):
    return render(request, 'appointment_confirmation.html')
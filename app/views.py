from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import AppointmentForm, PetForm
from .models import Pet, VaccinationRecord, Profile, MedicalRecord, Appointment


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

# Book appointment view
@login_required
def book_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.user = request.user  # assuming each appointment is linked to a user
            appointment.save()
            messages.success(request, "Appointment successfully booked.")
            return redirect('view_appointments')  # Redirect to view appointments
    else:
        form = AppointmentForm()

    return render(request, 'book_appointment.html', {'form': form})

# Manage pets view
@login_required
def manage_pets(request):
    if request.method == 'POST':
        form = PetForm(request.POST)
        if form.is_valid():
            pet = form.save(commit=False)
            pet.owner = request.user  # Assuming Pet model has a 'owner' field which is a ForeignKey to User
            pet.save()
            messages.success(request, "Pet information updated successfully.")
            return redirect('manage_pets')
    else:
        form = PetForm()
    pets = Pet.objects.filter(owner=request.user)  # Only show pets belonging to logged-in user
    return render(request, 'manage_pets.html', {'form': form, 'pets': pets})

# View appointments view
@login_required
def view_appointments(request):
    appointments = Appointment.objects.filter(user=request.user).order_by('date')
    return render(request, 'view_appointments.html', {'appointments': appointments})

# Vaccination records view
@login_required
def vaccination_records(request):
    vaccinations = VaccinationRecord.objects.filter(pet__owner=request.user).order_by('-date')
    return render(request, 'vaccination_records.html', {'vaccinations': vaccinations})

# Medical records view
@login_required
def medical_records(request):
    search_query = request.GET.get('search', '')
    if search_query:
        records = MedicalRecord.objects.filter(pet__owner=request.user, pet__name__icontains=search_query)
    else:
        records = MedicalRecord.objects.filter(pet__owner=request.user)
    return render(request, 'medical_records.html', {'records': records})

# Cancel appointment view
@login_required
def cancel_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id, user=request.user)
    appointment.delete()
    messages.success(request, 'Appointment successfully cancelled.')
    return redirect('dashboard')
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.utils import timezone
from datetime import datetime

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.username}'s profile"

# Signal to create or update a user profile whenever a user is created or updated
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        instance.profile.save()


class Pet(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="pets")
    name = models.CharField(max_length=100)
    breed = models.CharField(max_length=100)
    weight = models.FloatField()
    age = models.IntegerField(default=0)
    color = models.CharField(max_length=50, choices=settings.COLOR_CHOICES)
    custom_color = models.CharField(max_length=100, blank=True)  # Add custom_color field for 'other' color choice
    photo = models.ImageField(upload_to='pet_photos/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name}, the {self.breed}"


class Appointment(models.Model):
    TYPE_CHOICES = (
        ('checkup', 'Check-Up'),
        ('vaccination', 'Vaccination'),
        ('6_month_wellness', '6 month Wellness'),
        ('surgery', 'Surgery'),
        ('dental', 'Dental'),
        ('other', 'Other'),
    )
    
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name="appointments")
    date_time = models.DateTimeField()
    purpose = models.CharField(max_length=100)
    appointment_type = models.CharField(max_length=50, choices=TYPE_CHOICES, default='checkup')
    notes = models.TextField()
    status = models.CharField(max_length=100, default='scheduled')

    def __str__(self):
        return f"{self.date_time} - {self.get_appointment_type_display()} for {self.pet.name}"


def get_default_pet_id():
    pet = Pet.objects.first()  # Get the first pet
    if not pet:
        # Optionally create a pet if none exists
        pet = Pet.objects.create(name="Default Pet", breed="Unknown", weight=0, age=0, color="None")
    return pet.id

class MedicalRecord(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, default=get_default_pet_id)
    document = models.FileField(upload_to='medical_records/')
    uploaded_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Medical Record for {self.pet.name} on {self.uploaded_date.strftime('%Y-%m-%d')}"


class VaccinationRecord(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name="vaccination_records")
    document = models.FileField(upload_to='vaccination_records/', blank=True)
    uploaded_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.pet.name} vaccination record on {self.uploaded_date.strftime('%Y-%m-%d')}"

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.utils import timezone


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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name}, the {self.breed}"


class Appointment(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name="appointments")
    date_time = models.DateTimeField()
    purpose = models.CharField(max_length=100)
    notes = models.TextField()

    def __str__(self):
        return f"{self.date_time} for {self.pet.name}"

class MedicalRecord(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name="medical_records")
    date = models.DateField()
    treatment = models.CharField(max_length=100)
    diagnosis = models.TextField()
    medication = models.TextField()

    def __str__(self):
        return f"Medical Record for {self.pet.name} on {self.date}"

class VaccinationRecord(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name="vaccination_records")
    date = models.DateField()
    vaccine_type = models.CharField(max_length=100)
    notes = models.TextField()

    def __str__(self):
        return f"Vaccination on {self.date} for {self.pet.name}"


from django.urls import path
from .views import (
    register, login_view, logout_view, user_profile, dashboard,
    book_appointment, manage_pets, vaccination_records,
    edit_profile, delete_profile, settings_view, medical_records, pet_detail, 
    upload_photo, edit_phone_number, edit_email, edit_address, change_password, appointment_confirmation, 
    edit_appointment, cancel_appointment, appointments_view, appointment_details, upload_medical_record, upload_vaccination_record
)


urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', user_profile, name='profile'),
    path('settings/', settings_view, name='settings'),
    path('dashboard/', dashboard, name='dashboard'),
    path('book-appointment/', book_appointment, name='book_appointment'),
    path('manage-pets/', manage_pets, name='manage_pets'),
    path('vaccination-records/', vaccination_records, name='vaccination_records'),
    path('profile/edit/', edit_profile, name='edit_profile'),
    path('profile/delete/', delete_profile, name='delete_profile'),
    path('medical-records/', medical_records, name='medical_records'),
    path('pets/<int:pet_id>/', pet_detail, name='pet_detail'),
    path('pets/upload-photo/<int:pet_id>/', upload_photo, name='upload_photo'),
    path('profile/edit/email/', edit_email, name='edit_email'),
    path('profile/edit/address/', edit_address, name='edit_address'),
    path('profile/edit/password/', change_password, name='change_password'),
    path('profile/edit/phone/', edit_phone_number, name='edit_phone'),
    path('appointment-confirmation/', appointment_confirmation, name='appointment_confirmation'),
    path('appointments/edit/<int:id>/', edit_appointment, name='edit_appointment'),
    path('appointments/', appointments_view, name='appointments_view'),
    path('appointments/<int:id>/', appointment_details, name='appointment_details'),
    path('upload/', upload_medical_record, name='upload_medical_record'),
    path('upload-vaccination/', upload_vaccination_record, name='upload_vaccination_record'),
    path('appointments/cancel/<int:id>/', cancel_appointment, name='cancel_appointment'),
]
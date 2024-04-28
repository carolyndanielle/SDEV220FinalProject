from django.urls import path
from .views import (
    register, login_view, logout_view, user_profile, dashboard,
    book_appointment, manage_pets, view_appointments, vaccination_records,
    edit_profile, delete_profile, settings_view, medical_records, cancel_appointment
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
    path('appointments/', view_appointments, name='view_appointments'),
    path('vaccination-records/', vaccination_records, name='vaccination_records'),
    path('profile/edit/', edit_profile, name='edit_profile'),
    path('profile/delete/', delete_profile, name='delete_profile'),
    path('medical-records/', medical_records, name='medical_records'),
    path('cancel_appointment/', cancel_appointment, name='cancel_appointment'),
]

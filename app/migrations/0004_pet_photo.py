# Generated by Django 5.0.4 on 2024-05-01 03:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_appointment_appointment_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='pet',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='pet_photos/'),
        ),
    ]

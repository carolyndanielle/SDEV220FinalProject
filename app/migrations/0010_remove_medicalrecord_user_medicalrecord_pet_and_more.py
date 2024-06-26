# Generated by Django 5.0.4 on 2024-05-02 05:31

import app.models
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_remove_medicalrecord_date_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='medicalrecord',
            name='user',
        ),
        migrations.AddField(
            model_name='medicalrecord',
            name='pet',
            field=models.ForeignKey(default=app.models.get_default_pet_id, on_delete=django.db.models.deletion.CASCADE, to='app.pet'),
        ),
        migrations.AlterField(
            model_name='medicalrecord',
            name='document',
            field=models.FileField(upload_to='medical_records/'),
        ),
    ]

# Generated by Django 5.0.3 on 2024-04-11 15:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0002_alter_doctor_age_alter_doctor_unique_connect_token_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='connect_to_doctor_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]

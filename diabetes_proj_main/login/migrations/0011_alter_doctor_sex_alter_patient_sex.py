# Generated by Django 5.0.5 on 2024-05-19 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0010_remove_doctor_qr_code_remove_doctor_secret_key_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctor',
            name='sex',
            field=models.CharField(choices=[('Чоловіча', 'Чоловічий'), ('Жіноча', 'Жіночий')], max_length=20),
        ),
        migrations.AlterField(
            model_name='patient',
            name='sex',
            field=models.CharField(choices=[('Чоловіча', 'Чоловічий'), ('Жіноча', 'Жіночий')], max_length=20),
        ),
    ]

# Generated by Django 5.0.5 on 2024-05-10 20:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient_card', '0015_alter_analystype_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='analystype',
            name='name',
            field=models.CharField(blank=True, default='Інше', null=True),
        ),
    ]
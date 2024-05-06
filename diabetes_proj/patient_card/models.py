from django.db import models
from login.models import Patient

class GlucoseMeasurement(models.Model):

    CATEGORY = (
        ('Натщесердце', 'Натщесердце'),
        ('До сніданку', 'До сніданку'),
        ('Після сніданку', 'Після сніданку'),
        ('Перед перекусом', 'Перед перекусом'),
        ('Після перекусу', 'Після перекусу'),
        ('До обіду', 'До обіду'),
        ('Після обіду', 'Після обіду'),
        ('До вечері', 'До вечері'),
        ('Після вечері', 'Після вечері'),
        ('Перед сном', 'Перед сном'),
        ('Інше', 'Інше'),
    )

    glucose = models.DecimalField(max_digits=4, decimal_places=2, blank=False, null=False)
    glucose_measurement_category = models.CharField(choices=CATEGORY, blank=True, null=True)
    date_of_measurement = models.DateTimeField(auto_now_add=True, db_index=True)
    patient_id = models.ForeignKey(Patient, on_delete=models.CASCADE)

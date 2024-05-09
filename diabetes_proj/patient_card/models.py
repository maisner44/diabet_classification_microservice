from django.utils import timezone
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
    date_of_measurement = models.DateField()
    time_of_measurement = models.TimeField(default=timezone.now)
    patient_id = models.ForeignKey(Patient, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.glucose) + " Категорія: " + self.glucose_measurement_category
    
    class Meta:
        verbose_name = 'Замір глюкози'
        verbose_name_plural = 'Заміри глюкози'


class TypeOfActivity(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)

    def __str__(self):
        return 'Тип активності: ' + self.name
    
    class Meta:
        verbose_name = 'Тип активності'
        verbose_name_plural = 'Типи активності'


class PhysicalActivityMeasurement(models.Model):
    
    number_of_approaches = models.IntegerField(blank=True, null=False)
    type_of_activity = models.ForeignKey(TypeOfActivity, on_delete=models.PROTECT)
    time_of_activity = models.CharField(max_length=10, blank=True, null=True)
    commentary = models.TextField(max_length=1000, blank=True, null=True)
    patient_id = models.ForeignKey(Patient, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.patient_id} виконав {self.number_of_approaches} підходів у - {self.type_of_activity.name}'
    
    class Meta:
        verbose_name = 'Замір фізичної активності'
        verbose_name_plural = 'Заміри фізичної активності'
        

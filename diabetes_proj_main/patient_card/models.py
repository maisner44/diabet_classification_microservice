from typing import Iterable
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
    name = models.CharField(max_length=100, blank=False, null=False, unique=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Тип активності'
        verbose_name_plural = 'Типи активності'


class PhysicalActivityMeasurement(models.Model):
    
    number_of_approaches = models.IntegerField(blank=True, null=False)
    type_of_activity = models.ForeignKey(TypeOfActivity, on_delete=models.PROTECT)
    date_of_measurement = models.DateField(default=timezone.now)
    time_of_activity = models.TimeField(default=timezone.now)
    commentary = models.TextField(max_length=1000, blank=True, null=True)
    patient_id = models.ForeignKey(Patient, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.patient_id} виконав {self.number_of_approaches} підходів у - {self.type_of_activity.name}'
    
    class Meta:
        verbose_name = 'Замір фізичної активності'
        verbose_name_plural = 'Заміри фізичної активності'


class FoodItem(models.Model):

    name = models.CharField(max_length=200, blank=False, null=False, db_index=True)
    proteins = models.DecimalField(max_digits=6, decimal_places=2)
    fats = models.DecimalField(max_digits=6, decimal_places=2)
    carbohydrates = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"Їжа: {self.name}, білки - {self.proteins}, жири - {self.fats}, вуглеводи - {self.carbohydrates}"
    
    class Meta:
        verbose_name = 'Порція їжі'
        verbose_name_plural = 'Порції їжі'


class FoodMeasurement(models.Model):

    CATEGORY = (
        ('Сніданок', 'Сніданок'),
        ('Перекус', 'Перекус'),
        ('Обід', 'Обід'),
        ('Другий перекус', 'Другий перекус'),
        ('Вечеря', 'Вечеря'),
    )

    category = models.CharField(choices=CATEGORY, blank=False, null=False, default='Сніданок')
    insuline_dose_before = models.DecimalField(max_digits=5, decimal_places=2, blank=False, null=False)
    insuline_dose_after = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    date_of_measurement = models.DateField(default=timezone.now)
    time_of_eating = models.TimeField(default=timezone.now)
    bread_unit = models.IntegerField(blank=True, null=True)
    food_items = models.ManyToManyField(FoodItem)
    patient_id = models.ForeignKey(Patient, on_delete=models.CASCADE)

    def calculate_bread_unit(self):
        """
        Calculate bread unit (10-12g carbohydrate) for calculate insuline dose
        """
        if self.food_items:
            total_carbohydrates = 0
            for item in self.food_items.all():
                total_carbohydrates += item.carbohydrates
            bread_unit = total_carbohydrates/12
            return bread_unit
        else:
            return 0
    
    def calculate_dose(self):
        """
        Approximate calculation of insulin dose based on bread units
        """
        if self.bread_unit:
            return self.bread_unit
    

    def save(self, *args, **kwargs):
        """
        Overriding save method for init bread_unit after save measurement
        """
        self.insuline_dose_after = self.calculate_dose()
        super().save(*args, **kwargs)


    def __str__(self):
        return f'''
            Дата прийому їжі - {self.date_of_measurement}, час прийому - {self.time_of_eating} |
            Кількість хлібних одиниць - {self.bread_unit}, приблизна доля інсуліну - {self.insuline_dose_after}
        '''
    
    class Meta:
        verbose_name = 'Замір їжі'
        verbose_name_plural = 'Заміри їжі'


class InsulineDoseMeasurement(models.Model):

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

    category = models.CharField(choices=CATEGORY, blank=False, null=False)
    insuline_dose = models.DecimalField(max_digits=5, decimal_places=2, blank=False, null=False)
    date_of_measurement = models.DateField(default=timezone.now)
    time = models.TimeField(default=timezone.now)
    patient_id = models.ForeignKey(Patient, on_delete=models.CASCADE)

    def __str__(self):
        return  f'Категорія: {self.category}, станом на {self.time} вкололи {self.insuline_dose} ОД інсуліну'
    
    class Meta:
        verbose_name = 'Замір інсуліну'
        verbose_name_plural = 'Заміри інсуліну'


class AnalysType(models.Model):

    CATEGORY = (
        ('Загальний аналіз крові', 'Загальний аналіз крові'),
        ('Загальний аналіз сечі', 'Загальний аналіз сечі'),
        ('Аналіз крові на глюкозу', 'Аналіз крові на глюкозу'),
        ('Аналіз крові на глікований гемоглобин', 'Аналіз крові на глікований гемоглобин'),
        ('Аналіз С-пептид', 'Аналіз С-пептид'),
        ('Комплексний аналіз "Ліпідограма" ', 'Комплексний аналіз "Ліпідограма"'),
        ('Інше', 'Інше'),
    )
    name = models.CharField(choices=CATEGORY, blank=False, null=False, default='Інше')


class Analysis(models.Model):
    analysis = models.FileField(upload_to='patients-media/analysis')
    patient_id = models.ForeignKey(Patient, on_delete=models.CASCADE)
    date_of_measurement = models.DateField(default=timezone.now)
    analysis_type = models.ForeignKey(AnalysType, on_delete=models.PROTECT)

    def get_file_url(self):
        return self.analysis.url if self.analysis else None
    
    class Meta:
        verbose_name = 'Аналіз'
        verbose_name_plural = 'Аналізи'

        

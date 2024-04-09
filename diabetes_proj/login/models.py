from django.db import models
from django.contrib.auth.models import User, AbstractUser
from datetime import datetime

class DiaScreenUser(User):
    """
    Choices for sex options
    """
    
    MALE = 'Male'
    FEMALE = 'Female'
    SEX_CHOICES = (
        (MALE, 'Чоловічий'),
        (FEMALE, 'Жіночий'),
    )

    phone_number = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    sex = models.CharField(max_length=20, choices=SEX_CHOICES)
    age = models.IntegerField(db_index=True)
    patronymic = models.CharField(max_length=255, blank=True)

    def calculate_age(self):
        """
        Calculating a patient age by his date of birth
        """
        if self.date_of_birth.month > datetime.now().month:
            return datetime.now().year - self.date_of_birth.year - 1
        else:
            return datetime.now().year - self.date_of_birth.year
    
    def save(self, *args, **kwargs):
        """
        Overriding abstract user metod from django.contrib.auth.models which add additional
        functional when this model is save to database
        """
        if self.date_of_birth:
            self.age = self.calculate_age()
        super().save(*args, **kwargs)

    class Meta:
        abstract = True
        

# Create your models here.
class Patient(DiaScreenUser):
    """
    Choices for diabet type options
    """

    FIRST_TYPE = 1
    SECOND_TYPE = 2
    NULL_TYPE = 0
    DIABETES_TYPE_CHOICES = (
        (FIRST_TYPE, '1 тип'),
        (SECOND_TYPE, '2 тип'),
        (NULL_TYPE, 'відсутній')
    )

    height = models.DecimalField(max_digits=6, decimal_places=2)
    weight = models.DecimalField(max_digits=6, decimal_places=2)
    body_mass_index = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    connect_to_doctor_date = models.DateTimeField(blank=True)
    diabet_type = models.CharField(max_length=10, choices=DIABETES_TYPE_CHOICES, db_index=True, default=NULL_TYPE)
    is_oninsuline = models.BooleanField(db_index=True)

    def calculate_BMI(self):
        """
        Calculate body mass index for patient from his measurements
        """
        return self.weight / (self.height ** 2)
    
    
    def save(self, *args, **kwargs):
        """
        Overriding abstract user metod from django.contrib.auth.models which add additional
        functional when this model is save to database
        """
        if self.weight and self.height:
            self.body_mass_index = self.calculate_BMI()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.first_name + " " + self.last_name
    


class Doctor(DiaScreenUser):
        
        work_experience = models.IntegerField()
        
   

    
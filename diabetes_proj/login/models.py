from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.utils.translation import gettext_lazy as _
from datetime import datetime
import uuid


class Adress(models.Model):
    """
    Abstract model for users and organizations adresses
    """
    country = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    street = models.CharField(max_length=50)
    house_number = models.IntegerField()
    postal_code = models.CharField(max_length=50)


class Organization(models.Model):
    """
    Organization model for Doctor.This is organization where doctor is currently working
    """
    organization_name = models.CharField(max_length=255, db_index=True)
    organization_logo = models.ImageField(blank=True)
    organization_phone = models.CharField(max_length=255)
    organization_email = models.EmailField(_("Електронна пошта"))
    organization_description = models.TextField()
    organization_website_url = models.URLField(blank=True)
    adress_id = models.ForeignKey(Adress, on_delete=models.SET_NULL, db_index=True)


class DiaScreenUser(User):
    """
    Choices for sex options for user
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


class Doctor(DiaScreenUser):
        
    work_experience = models.IntegerField(db_index=True)
    specialization = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    certificate_or_diploma = models.FileField(upload_to='certificates/')
    unique_connect_token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    about = models.TextField()
    organization_id = models.ForeignKey(Organization, on_delete=models.SET_NULL, db_index=True, blank=True)

    def __str__(self):
        return self.first_name + " " + self.last_name + " " + self.unique_connect_token


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
    doctor_id = models.ForeignKey(Doctor, on_delete=models.PROTECT, db_index=True, blank=True)
    adress_id = models.ForeignKey(Adress, on_delete=models.SET_NULL, blank=True, db_index=True, null=True)

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
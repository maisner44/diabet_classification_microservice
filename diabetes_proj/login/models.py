from django.db import models
from django.contrib.auth.models import User, AbstractUser, Group
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from datetime import datetime
import uuid
from django.contrib.auth.hashers import make_password
from .utils.TOTP import *


class Adress(models.Model):
    """
    Abstract model for users and organizations adresses
    """
    country = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    street = models.CharField(max_length=50, blank=True, null=True)
    house_number = models.IntegerField(blank=True, null=True)
    postal_code = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        verbose_name = "Adress"
        verbose_name_plural = "Adresses"


class Organization(models.Model):
    """
    Organization model for Doctor.This is organization where doctor is currently working
    """
    organization_name = models.CharField(max_length=255, db_index=True, blank=True, null=True)
    organization_logo = models.ImageField(upload_to='organization-logos/',blank=True, null=True)
    organization_phone = models.CharField(max_length=255, blank=True, null=True)
    organization_email = models.EmailField(_("Електронна пошта"), blank=True, null=True)
    organization_description = models.TextField(blank=True, null=True)
    organization_website_url = models.URLField(blank=True, null=True)
    adress_id = models.ForeignKey(Adress, on_delete=models.SET_NULL, db_index=True, null=True, blank=True)

    class Meta:
        ordering = ['organization_name']
        verbose_name = "Organization"
        verbose_name_plural = "Organizations"


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

    phone_number = models.CharField(max_length=255, unique=True)
    date_of_birth = models.DateField()
    sex = models.CharField(max_length=20, choices=SEX_CHOICES)
    age = models.IntegerField(db_index=True, blank=True, null=True)
    patronymic = models.CharField(max_length=255, blank=True)
    avatar = models.ImageField(default='placeholder-img.png', upload_to='profile-pics/', blank=True, null=True)
    two_factor_enabled = models.BooleanField(default=False)
    secret_key = models.CharField(max_length=255, blank=True, null=True)
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True)

    def enable_two_factor(self):
        if not self.two_factor_enabled:
            self.two_factor_enabled = True
            self.secret_key = generate_secret_key()
            self.generate_qr_code()
            self.save()

    def disable_two_factor(self):
        if self.two_factor_enabled:
            self.two_factor_enabled = False
            self.secret_key = None
            self.qr_code = None
            self.save()

    def generate_qr_code(self):
        uri = generate_provision_url(self.username)
        if uri:
            img = generate_qrcode(uri)
            self.qr_code.save(f'qr_code_{self.username}.png', img, save=False)

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
        if self.pk is None:
            self.password = make_password(self.password)
        else:
            old_instance = type(self).objects.get(pk=self.pk)
            if self.password != old_instance.password:
                self.password = make_password(self.password)

        if self.date_of_birth:
            self.age = self.calculate_age()
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['last_name', 'age']
        abstract = True


class Doctor(DiaScreenUser):
    """
    Doctor model
    """  
    work_experience = models.IntegerField(db_index=True)
    specialization = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    certificate_or_diploma = models.FileField(upload_to='certificates/')
    unique_connect_token = models.UUIDField(default=uuid.uuid4, editable=True, unique=True)
    about = models.TextField(blank=True, null=True)
    organization_id = models.ForeignKey(Organization, on_delete=models.SET_NULL, db_index=True, blank=True, null=True)

    def __str__(self):
        return self.first_name + " " + self.last_name
    
    def save(self, *args, **kwargs):
        """
        Overriding abstract user metod from django.contrib.auth.models which add additional
        functional when this model is save to database
        """
        super().save(*args, **kwargs)
        group = Group.objects.get(name='Doctors')
        group.user_set.add(self)
    
    class Meta:
        ordering = ['work_experience']
        verbose_name = "Doctor"
        verbose_name_plural = "Doctors"


class Patient(DiaScreenUser):
    """
    Choices for diabet type options
    """
    FIRST_TYPE = '1'
    SECOND_TYPE = '2'
    NULL_TYPE = 'null'
    DIABETES_TYPE_CHOICES = (
        (FIRST_TYPE, '1 тип'),
        (SECOND_TYPE, '2 тип'),
        (NULL_TYPE, 'Відсутній'),
    )

    height = models.DecimalField(max_digits=6, decimal_places=2)
    weight = models.DecimalField(max_digits=6, decimal_places=2)
    body_mass_index = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    connect_to_doctor_date = models.DateTimeField(blank=True, null=True)
    diabet_type = models.CharField(max_length=10, choices=DIABETES_TYPE_CHOICES, default=NULL_TYPE)
    is_oninsuline = models.BooleanField(db_index=True, null=True)
    doctor_id = models.ForeignKey(Doctor, on_delete=models.SET_NULL, blank=True, null=True)
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
        if self.diabet_type == self.FIRST_TYPE:
            self.is_oninsuline = True
        if self.doctor_id and not self.connect_to_doctor_date:
            self.connect_to_doctor_date = timezone.now()
        super(Patient,self).save(*args, **kwargs)
        group = Group.objects.get(name='Patients')
        group.user_set.add(self)


    def __str__(self):
        return self.first_name + " " + self.last_name
    
    class Meta:
        ordering = ['connect_to_doctor_date', 'diabet_type', 'is_oninsuline']
        verbose_name = "Patient"
        verbose_name_plural = "Patients"
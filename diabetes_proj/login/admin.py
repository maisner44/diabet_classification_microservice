from django.contrib import admin
from .models import Adress, Organization, Patient, Doctor

# Register your models here.
class AdressAdmin(admin.ModelAdmin):

    list_display = [
        'country',
        'city',
        'street',
        'house_number',
        'postal_code',
    ]
    list_filter = ['country','city','street']
    search_fields = ['city','street']


class OrganizationAdmin(admin.ModelAdmin):
    
    list_display = [
        'organization_name',
        'organization_phone',
        'organization_email',
        'organization_website_url',
        'adress_id',
    ]
    list_filter = ['organization_name']
    search_fields = ['organization_name']


class PatientAdmin(admin.ModelAdmin):
    list_display = [
        'first_name', 
        'last_name',
        'password',
        'age', 
        'email', 
        'username', 
        'height',
        'weight',
        'body_mass_index',
        'diabet_type',
        'is_oninsuline',
        'doctor_id',
        'adress_id',
    ] 
    list_filter = ['diabet_type', 'is_oninsuline']
    search_fields = ['first_name', 'last_name', 'username','email']


class DoctorAdmin(admin.ModelAdmin):
    list_display = [
        'first_name', 
        'last_name',
        'password',
        'email', 
        'username',
        'work_experience',
        'specialization',
        'category',
        'unique_connect_token',
        'organization_id',
    ] 
    list_filter = ['work_experience']
    search_fields = ['first_name', 'last_name', 'username','email']


admin.site.register(Adress, AdressAdmin)
admin.site.register(Organization, OrganizationAdmin)
admin.site.register(Patient, PatientAdmin)
admin.site.register(Doctor, DoctorAdmin)
from login.models import Patient, Doctor, Adress, Organization
from patient_card.models import GlucoseMeasurement, PhysicalActivityMeasurement
from rest_framework import serializers

class PatientCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ["username", "password", "date_of_birth", "first_name", "last_name", "patronymic", "height", "weight",
                  "diabet_type", "email", "phone_number"]
        

class PatientListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ["username", "first_name", "last_name", "patronymic", "height", "weight", "diabet_type", "body_mass_index"]

class GlucoseSerializer(serializers.ModelSerializer):
    class Meta:
        model = GlucoseMeasurement
        exclude = ["patient_id"]
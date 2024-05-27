from login.models import Patient, Doctor, Adress, Organization
from patient_card.models import GlucoseMeasurement, PhysicalActivityMeasurement, TypeOfActivity, InsulineDoseMeasurement, FoodItem, FoodMeasurement
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


class TypeOfActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeOfActivity
        fields = ['id', 'name']

class PhysicalActivityMeasurementSerializer(serializers.ModelSerializer):
    type_of_activity = serializers.PrimaryKeyRelatedField(queryset=TypeOfActivity.objects.all())
    
    class Meta:
        model = PhysicalActivityMeasurement
        exclude = ["patient_id"]

class InsulineDoseSerializer(serializers.ModelSerializer):
    class Meta:
        model = InsulineDoseMeasurement
        exclude = ["patient_id"]


class FoodItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodItem
        exclude = ["id"]

class FoodMeasurementSerializer(serializers.ModelSerializer):
    food_items = FoodItemSerializer(many=True)
    class Meta:
        model = FoodMeasurement
        exclude = ["patient_id"]

    def create(self, validated_data):
        food_items_data = validated_data.pop('food_items')
        food_measurement = FoodMeasurement.objects.create(**validated_data)
        food_measurement.food_items.set(food_items_data)
        food_measurement.save()
        return food_measurement

from rest_framework import serializers
from .models import GlucoseMeasurement

class GlucoseMeasurementSerializer(serializers.ModelSerializer):
    class Meta:
        model = GlucoseMeasurement
        fields = "__all__"
    
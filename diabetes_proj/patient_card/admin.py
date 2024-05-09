from django.contrib import admin
from .models import GlucoseMeasurement, TypeOfActivity, PhysicalActivityMeasurement

admin.site.register(GlucoseMeasurement)
admin.site.register(TypeOfActivity)
admin.site.register(PhysicalActivityMeasurement)
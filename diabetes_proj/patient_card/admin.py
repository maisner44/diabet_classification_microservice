from django.contrib import admin
from .models import GlucoseMeasurement, TypeOfActivity, PhysicalActivityMeasurement, FoodMeasurement, FoodItem, InsulineDoseMeasurement
from .models import Analysis, AnalysType

admin.site.register(GlucoseMeasurement)
admin.site.register(TypeOfActivity)
admin.site.register(PhysicalActivityMeasurement)
admin.site.register(FoodMeasurement)
admin.site.register(FoodItem)
admin.site.register(InsulineDoseMeasurement)
admin.site.register(AnalysType)
admin.site.register(Analysis)

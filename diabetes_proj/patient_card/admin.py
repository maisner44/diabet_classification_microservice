from django.contrib import admin
from .models import GlucoseMeasurement, TypeOfActivity, PhysicalActivityMeasurement, FoodMeasurement, FoodItem

admin.site.register(GlucoseMeasurement)
admin.site.register(TypeOfActivity)
admin.site.register(PhysicalActivityMeasurement)
admin.site.register(FoodMeasurement)
admin.site.register(FoodItem)
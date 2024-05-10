from django.urls import path
from .views import GlucoseMeasurmentView, PhysicalMeasurementView, FoodMeasurementView, InsulineDoseView

urlpatterns = [
    path('<int:patient_id>', GlucoseMeasurmentView.as_view(), name='patient_card'),
    path('physics/<int:patient_id>', PhysicalMeasurementView.as_view(), name='patient_physics'),
    path('food/<int:patient_id>', FoodMeasurementView.as_view(), name='patient_food'),
    path('insuline-therapy/<int:patient_id>', InsulineDoseView.as_view(), name='patient_insuline'),
]
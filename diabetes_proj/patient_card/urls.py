from django.urls import path
from .views import GlucoseMeasurmentView, PhysicalMeasurementView

urlpatterns = [
    path('<int:patient_id>', GlucoseMeasurmentView.as_view(), name='patient_card'),
    path('physics/<int:patient_id>', PhysicalMeasurementView.as_view(), name='patient_physics')
]
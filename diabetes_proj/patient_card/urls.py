from django.urls import path
from .views import GlucoseMeasurmentView, PhysicalMeasurementView, FoodMeasurementView, InsulineDoseView, AnalysisLoadView, download_pdf

urlpatterns = [
    path('<int:patient_id>', GlucoseMeasurmentView.as_view(), name='patient_card'),
    path('physics/<int:patient_id>', PhysicalMeasurementView.as_view(), name='patient_physics'),
    path('food/<int:patient_id>', FoodMeasurementView.as_view(), name='patient_food'),
    path('insuline-therapy/<int:patient_id>', InsulineDoseView.as_view(), name='patient_insuline'),
    path('analysis/<int:patient_id>', AnalysisLoadView.as_view(), name='patient_analysis'),
    path('download-pdf/<int:patient_id>', download_pdf, name='analysis_download')
]
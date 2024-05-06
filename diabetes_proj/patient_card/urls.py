from django.urls import path
from .views import patient_card

urlpatterns = [
    path('<int:patient_id>', patient_card, name='patient_card'),
]
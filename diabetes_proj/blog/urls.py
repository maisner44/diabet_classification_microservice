from django.urls import path
from .views import InformationPanel

urlpatterns = [
    path('', InformationPanel.as_view(), name='information')
]
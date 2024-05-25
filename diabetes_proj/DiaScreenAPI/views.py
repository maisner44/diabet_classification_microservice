from django.shortcuts import render, get_object_or_404
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from login.models import Patient
from patient_card.models import GlucoseMeasurement
from .serializers import PatientCreateSerializer, PatientListSerializer, GlucoseSerializer

class PatientCreateView(generics.CreateAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientCreateSerializer
    permission_classes = [IsAuthenticated]

class PatientListView(generics.ListAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientListSerializer
    permission_classes = [IsAuthenticated]
   
class PatientByDoctorView(generics.ListAPIView):
    serializer_class = PatientListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        doctor_id = self.kwargs['doctor_id']
        return Patient.objects.filter(doctor_id=doctor_id)
    
class GlucoseCreateListView(generics.ListCreateAPIView):
    queryset = GlucoseMeasurement.objects.all()
    serializer_class = GlucoseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        username = self.kwargs['username']
        patient = get_object_or_404(Patient, username=username)
        return GlucoseMeasurement.objects.filter(patient_id=patient.id)
    
    def perform_create(self, serializer):
        username = self.kwargs['username']
        patient = get_object_or_404(Patient, username=username)
        serializer.save(patient_id = patient)
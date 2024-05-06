from django.shortcuts import render

def patient_card(request, patient_id):
    
    return render(request, 'patient_card.html')

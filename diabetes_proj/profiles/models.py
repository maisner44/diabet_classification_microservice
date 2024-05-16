from django.db import models
from django.contrib.auth.models import User
from login.models import Doctor, Patient

class DoctorsProfileFeedback(models.Model):
    doctor_id = models.ForeignKey(Doctor, on_delete=models.CASCADE, db_index=True, null=True, blank=True)
    patient_id = models.ForeignKey(Patient, on_delete=models.PROTECT, db_index=True, null=True, blank=True)
    feedback_text = models.TextField(max_length=1000, null=True, blank=True)
    date_of_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['doctor_id', 'patient_id']

    def __str__(self):
        return f'''
        Відгук від {self.patient_id}, до лікаря {self.doctor_id}
        створений о {self.date_of_created} та містить текст {self.feedback_text}
        '''


class TechSupportTicket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    text = models.TextField(max_length=2000, blank=False, null=False)
    email = models.EmailField()
    img = models.ImageField(upload_to='tech-support/tickets/', blank=True, null=True)
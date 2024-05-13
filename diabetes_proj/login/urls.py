from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import enable_two_auth

urlpatterns = [
    path('registration', views.registration, name='registration'),
    path('registration/patients', views.register_patient, name='patient_register'),
    path('registration/doctors', views.register_doctor, name='doctor_register'),
    path('login', views.user_login, name='login'),
    path('reset-password', auth_views.PasswordResetView.as_view(template_name = 'login/reset-password.html'), name='password_reset'),
    path('reset-password-send', auth_views.PasswordResetDoneView.as_view(template_name = 'login/reset-password-send.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name = 'login/reset-password-confirm.html'), name='password_reset_confirm'),
    path('reset-password-complete', auth_views.PasswordResetCompleteView.as_view(template_name = 'login/reset-password-complete.html'), name='password_reset_complete'),
    path('logout', auth_views.LogoutView.as_view(next_page = 'login'), name='logout'),
    path('enable-two-auth', enable_two_auth, name='enable_two_auth'),
]
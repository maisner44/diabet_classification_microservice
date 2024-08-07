"""
URL configuration for diabetes_proj project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from profiles.views import send_support_ticket

urlpatterns = [
    path('', TemplateView.as_view(template_name = 'index.html'), name='home'),
    path('admin/', admin.site.urls),
    path('privacy-policy', TemplateView.as_view(template_name = 'privacy_policy.html'), name='policy'),
    path('api-view', TemplateView.as_view(template_name = 'api/api.html'), name='api'),
    path('support/', send_support_ticket, name='support'),
    path('accounts/', include('login.urls')),
    path('doctor-search/', include('doctor_search.urls')),
    path('profile/', include('profiles.urls')),
    path('blog/', include('blog.urls')),
    path('card/', include('patient_card.urls')),
    path('chat/', include('chat.urls')),
    path('api/', include('DiaScreenAPI.urls')),
    path("__debug__/", include("debug_toolbar.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.contrib import admin
from django.urls import path
from medico.views import medBoard, contaMedico, mostrarPacientes
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', medBoard, name='medico_dash'),
    path('medico/conta/', contaMedico, name='conta_medico'),
    path('medico/meus-pacientes/', mostrarPacientes, name='meus_pacientes'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
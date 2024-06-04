from django.contrib import admin
from django.urls import path
from medico.views import medBoard, contaMedico, mostrarPacientes, document_list, info_prontuario, init_prontuario, dadosPaciente, concluirConsulta, mostrarConsultas, addDocument
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', medBoard, name='medico_dash'),
    path('medico/conta/', contaMedico, name='conta_medico'),
    path('medico/meus-pacientes/', mostrarPacientes, name='meus_pacientes'),
    path('paciente/<int:id>/prontuario/', document_list, name='prontuario_med'),
    path('paciente/<int:id>/prontuario/init', init_prontuario, name='init_prontuario_med'),
    path('paciente/<int:id>/prontuario/info', info_prontuario, name='info_prontuario_med'),
    path('paciente/<int:id>/', dadosPaciente, name='paciente_med'),
    path('consultas', mostrarConsultas, name='consultas_med'),
    path('consulta/<int:id>/cancelar_consulta/', concluirConsulta, name='concluir_consulta'),
    path('paciente/documento/add/', addDocument, name='add_doc_med'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
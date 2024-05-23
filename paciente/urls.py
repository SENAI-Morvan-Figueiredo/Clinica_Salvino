from django.contrib import admin
from django.urls import path
from paciente.views import pagamento_paciente, agendamento_paciente, add_cartao, add_convenio, mostrarCartoes, delete_cartao
from paciente.views import pacienteBoard, contaPaciente, mostrarPacienteConvenio, cadConvPaciente
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', pacienteBoard, name='paciente_dash'),
    path('conta/', contaPaciente, name='conta_paciente'),
    path('pagamento/', pagamento_paciente, name='pagamento_paciente'),
    path('agendamento/', agendamento_paciente, name='agendamento_paciente'),
    path('cartoes/add', add_cartao, name='add_cartao_paciente'),
    path('convenios/add ', add_convenio, name='add_convenio_paciente'),
    path('cartoes/', mostrarCartoes, name='cartoes_paciente'),
    path('convenios/', mostrarPacienteConvenio, name='convenios_paciente'),
    path('paciente/<int:id>/cadastro_convenios/add', cadConvPaciente, name='adicionar_convenio_paciente'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
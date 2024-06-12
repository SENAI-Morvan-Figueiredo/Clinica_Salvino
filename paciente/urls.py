from django.contrib import admin
from django.urls import path
from paciente.views import pacienteBoard, contaPaciente, mostrarPacienteConvenio, pagamento_paciente, agendamento_paciente, add_cartao, add_convenio, mostrarCartoes, delete_cartao, delete_convenio, pagarConsultaBol, pagarConsultaCard, pagarConsultaConv, payPix, mostrarConsultas, cancelarConsulta, mostrarContas, mostrarBoleto, chavePix, document_list, document, encaminha, bio, anexo, anexos_list
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', pacienteBoard, name='paciente_dash'),
    path('conta/', contaPaciente, name='conta_paciente'),
    path('pagamento/', pagamento_paciente, name='pagamento_paciente'),
    path('agendamento/', agendamento_paciente, name='agendamento_paciente'),
    path('cartoes/', mostrarCartoes, name='cartoes_paciente'),
    path('cartoes/add', add_cartao, name='add_cartao_paciente'),
    path('cartao/<int:id>/delete', delete_cartao, name='delete_cartao_paciente'),
    path('convenios/', mostrarPacienteConvenio, name='convenios_paciente'),
    path('convenios/add ', add_convenio, name='add_convenio_paciente'),
    path('convenio/<int:id>/delete', delete_convenio, name='delete_convenio_paciente'),
    path('pagamento/', pagamento_paciente, name='pay_paciente'),
    path('pagamento/cartao', pagarConsultaCard, name='pay_card_paciente'),
    path('pagamento/convenio', pagarConsultaConv, name='pay_conv_paciente'),
    path('pagamento/boleto', pagarConsultaBol, name='pay_bol_paciente'),
    path('pagamento/pix', payPix, name='pay_pix_paciente'),
    path('consultas', mostrarConsultas, name='consultas_paciente'),
    path('consultas/<int:id>/cancelar_consulta/', cancelarConsulta, name='cancelar_consulta_paciente'),
    path('consulta/<int:id>/anexos/', anexos_list, name='an_list_paciente'),
    path('pix/<int:id>', chavePix, name='pix_paciente'),
    path('boleto/<int:id>', mostrarBoleto, name='boleto_paciente'),
    path('contas/', mostrarContas, name='financeiro_paciente'),
    path('prontuario/', document_list, name='prontuario_paciente'),
    path('documento/<int:id>/', document, name='doc_paciente'),
    path('encaminhamento/<int:id>/', encaminha, name='en_paciente'),
    path('bioimpedancia/<int:id>/', bio, name='bio_paciente'),
    path('anexo/<int:id>/', anexo, name='an_paciente'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
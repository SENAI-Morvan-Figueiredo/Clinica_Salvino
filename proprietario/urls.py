from django.urls import path
from proprietario.views import proprietyBoard, contaProprietario, mostrarPacientes, mostrarFuncionarios, dadosFuncionario, deleteFuncionario, dadosPaciente, deletePaciente, addFuncionario, addPaciente, addRecep, addMedico, mostrarEspecialidades, dadosEspecialidade, addEspecialidade, deleteEspecialidade, marcarConsulta, mostrarConsultas, cancelarConsulta, adicionarBandeira, deleteBandeira, mostrarBandeiras, mostrarCartoes, adicionarCartoes, deleteCartao, addFornecedorConvenio, mostrarConvenios, deleteConvenio, mostrarPlano, addPlano, deletePlano, mostrarPacienteConvenio, cadConvPaciente, delPacienteConv, mostrarFichas, abrirFicha

urlpatterns = [
    path('', proprietyBoard, name='proprietario_dash'),
    path('conta/', contaProprietario, name= 'conta_proprietario'),
    path('pacientes', mostrarPacientes, name= 'pacientes'),
    path('pacientes/add', addPaciente, name= 'adicionar_pacientes'),
    path('paciente/<int:id>/', dadosPaciente, name='paciente'),
    path('paciente/<int:id>/delete/', deletePaciente, name='delete_paciente'),
    path('paciente/<int:id>/cartoes/', mostrarCartoes, name='cartoes_prop'),
    path('paciente/<int:id>/cartoes/add', adicionarCartoes, name='adicionar_cartoes'),
    path('cartao/<int:id>/delete', deleteCartao, name='deletar_cartao'),
    path('paciente/<int:id>/cadastro_convenios/', mostrarPacienteConvenio, name='convenios_paciente_prop'),
    path('paciente/<int:id>/cadastro_convenios/add', cadConvPaciente, name='adicionar_convenio_paciente'),
    path('cadastro_convenio/<int:id>/delete', delPacienteConv, name='deletar_convenio_paciente'),
    path('funcionarios', mostrarFuncionarios, name= 'funcionarios'),
    path('funcionarios/add', addFuncionario, name= 'adicionar_funcionarios'),
    path('funcionarios/add/recepcionista', addRecep, name= 'adicionar_recep'),
    path('funcionarios/add/medico', addMedico, name= 'adicionar_medico'),
    path('funcionario/<int:id>/', dadosFuncionario, name='funcionario'),
    path('funcionario/<int:id>/delete/', deleteFuncionario, name='delete_funcionario'),
    path('especialidades', mostrarEspecialidades, name='especialidades'),
    path('especialidades/add', addEspecialidade, name='adicionar_especialidade'),
    path('especialidade/<int:id>/', dadosEspecialidade, name='especialidade'),
    path('especialidade/<int:id>/delete/', deleteEspecialidade, name='delete_especialidade'),
    path('agendamento/', marcarConsulta, name='agendamento'),
    path('consultas', mostrarConsultas, name='consultas'),
    path('consultas/<int:id>/cancelar/', cancelarConsulta, name='cancelar_consulta'),
    path('bandeiras/', mostrarBandeiras, name='bandeiras'),
    path('bandeiras/add', adicionarBandeira, name='adicionar_bandeira'),
    path('bandeira/<int:id>/dele/', deleteBandeira, name='deletar_bandeira'),
    path('convenios/', mostrarConvenios, name='convenios'),
    path('convenios/add/', addFornecedorConvenio, name='adicionar_convenio'),
    path('convenio/<int:id>/delete/', deleteConvenio, name='deletar_convenio'),
    path('convenio/<int:id>/planos/', mostrarPlano, name='planos_convenio'),
    path('convenio/<int:id>/planos/add/', addPlano, name='adicionar_plano'),
    path('plano/<int:id>/delete/', deletePlano, name='deletar_plano'),
    path('fichas/', mostrarFichas, name='fichas_prop'),
    path('ficha/<int:id>/abrir', abrirFicha, name='abrir_ficha_prop'),
]

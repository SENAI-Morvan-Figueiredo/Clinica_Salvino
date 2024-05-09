from django.urls import path
from proprietario.views import proprietyBoard, contaProprietario, mostrarPacientes, mostrarFuncionarios, dadosFuncionario, deleteFuncionario, dadosPaciente, deletePaciente, addFuncionario, addPaciente, addRecep, addMedico, mostrarEspecialidades, dadosEspecialidade, addEspecialidade, deleteEspecialidade, marcarConsulta, mostrarConsultas, cancelarConsulta, adicionarBandeira, deleteBandeira, mostrarBandeiras

urlpatterns = [
    path('', proprietyBoard, name='proprietario_dash'),
    path('conta/', contaProprietario, name= 'conta_proprietario'),
    path('pacientes', mostrarPacientes, name= 'pacientes'),
    path('pacientes/add', addPaciente, name= 'adicionar_pacientes'),
    path('paciente/<int:id>/', dadosPaciente, name='paciente'),
    path('paciente/<int:id>/delete/', deletePaciente, name='delete_paciente'),
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
]

from django.contrib import admin
from django.urls import path
from clinica.views import home, contact_us, nutris, login, forgot, change_email, change_password, logout_user
from paciente.views import register
from medico.views import medBoard, contaMedico
from recept.views import receptBoard, contaRecept
from proprietario.views import proprietyBoard, contaProprietario, mostrarPacientes, mostrarFuncionarios, dadosFuncionario, deleteFuncionario, dadosPaciente, deletePaciente, addFuncionario, addPaciente, addRecep, addMecico, mostrarEspecialidades
from paciente.views import pacienteBoard, contaPaciente

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
    path('funcionarios/add/medico', addMecico, name= 'adicionar_medico'),
    path('funcionario/<int:id>/', dadosFuncionario, name='funcionario'),
    path('funcionario/<int:id>/delete/', deleteFuncionario, name='delete_funcionario'),
    path('especialidades', mostrarEspecialidades, name='especialidades')
]

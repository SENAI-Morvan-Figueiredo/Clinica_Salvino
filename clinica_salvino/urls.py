from django.contrib import admin
from django.urls import path, include
from clinica.views import home, contact_us, nutris, login, forgot, change_email, change_password, logout_user
from paciente.views import register
from medico.views import medBoard, contaMedico
from recept.views import receptBoard, contaRecept
import proprietario.urls
from proprietario.views import proprietyBoard, contaProprietario, mostrarPacientes, mostrarFuncionarios, dadosFuncionario, deleteFuncionario, dadosPaciente, deletePaciente, addFuncionario, addPaciente, addRecep, addMecico
from paciente.views import pacienteBoard, contaPaciente

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('contact/', contact_us, name='contact'),
    path('nutris/', nutris, name='nutris'),
    path('login/', login, name='login'),
    path('cadastro/', register, name='cadastro'),
    path('esqueci-senha/', forgot, name='esqueci-senha'),
    path('alterar-email/', change_email, name='alterar-email'),
    path('alterar-senha/', change_password, name='alterar-senha'),
    path('proprietario/', include(proprietario.urls)),
    path('paciente/', pacienteBoard, name='paciente_dash'),
    path('medico/', medBoard, name='medico_dash'),
    path('recepcionista/', receptBoard, name='recepcionista_dash'),
    path('logout/', logout_user, name='logout'),
    path('paciente/conta/', contaPaciente, name='conta_paciente'),
    path('medico/conta/', contaMedico, name='conta_medico'),
    path('recepcionista/conta', contaRecept, name='conta_recepcionista'),
]

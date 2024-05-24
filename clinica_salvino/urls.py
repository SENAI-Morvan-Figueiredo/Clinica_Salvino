from django.contrib import admin
from django.urls import path, include
from clinica.views import home, contact_us, nutris, login, forgot, change_email, change_password, logout_user, get_available_times
from paciente.views import register
from medico.views import medBoard, contaMedico
from recept.views import receptBoard, contaRecept
import proprietario.urls
import paciente.urls
from paciente.views import pacienteBoard, contaPaciente
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('contact/', contact_us, name='contact'),
    path('nutris/', nutris, name='nutris'),
    path('login/', login, name='login'),
    path('cadastro/', register, name='cadastro'),
    path('esqueci-senha/', forgot, name='esqueci-senha'),
    path('alterar-email/', change_email, name='alterar-email'),
    path('alterar_senha/', change_password, name='alterar_senha'),
    path('proprietario/', include(proprietario.urls)),
    path('paciente/', include(paciente.urls)),
    path('medico/', medBoard, name='medico_dash'),
    path('recepcionista/', receptBoard, name='recepcionista_dash'),
    path('logout/', logout_user, name='logout'),
    path('medico/conta/', contaMedico, name='conta_medico'),
    path('recepcionista/conta', contaRecept, name='conta_recepcionista'),
    path('get_available_times/', get_available_times, name='get_available_times'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.contrib import admin
from django.urls import path, include
from clinica.views import home, contact_us, nutris, login, change_email, change_password, logout_user, get_available_times, password_reset_request, reset_password
from paciente.views import register
from medico.views import medBoard, contaMedico
from recept.views import receptBoard, contaRecept
import proprietario.urls
import paciente.urls
from paciente.views import pacienteBoard, contaPaciente
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('contact/', contact_us, name='contact'),
    path('nutris/', nutris, name='nutris'),
    path('login/', login, name='login'),
    path('cadastro/', register, name='cadastro'),
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
    path('esqueci_senha/', password_reset_request, name='password_reset'),
    path('reset/<uidb64>/<token>/', reset_password, name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/reset_email_concluido.html'), name='password_reset_done'),
    path('email/enviado/', auth_views.PasswordResetDoneView.as_view(template_name='registration/reset_senha_concluido.html'), name='password_reset_complete'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
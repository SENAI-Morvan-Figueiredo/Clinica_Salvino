"""
URL configuration for clinica_salvino project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from clinica.views import home, contact_us, nutris, login, forgot, change_email, change_password, proprietario
from paciente.views import register, card

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
    path('proprietario', proprietario, name='proprietario'),
    path('card/', card, name='card'),
]

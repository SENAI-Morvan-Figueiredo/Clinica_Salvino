from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from paciente.models import Paciente
from medico.models import Medico
from recept.models import Recepcionista
from itertools import chain

# Create your views here.
@login_required 
def proprietyBoard(request):
    proprietario = request.user.proprietario
    return render(request, 'proprietario.html', {'proprietario': proprietario})

def contaProprietario(request):
    proprietario = request.user.proprietario
    return render(request, 'myaccount_proprietario.html', {'proprietario': proprietario})

def mostrarPacientes(request):
    pacientes = Paciente.objects.all()
    return render(request, 'pacientes_list (prop).html', {'pacientes': pacientes})

def mostrarFuncionarios(request):
    medicos = Medico.objects.all()
    recepcionistas = Recepcionista.objects.all()

    funcionarios = list(chain(medicos, recepcionistas))

    return render(request, 'funcionarios_list (prop).html', {'funcionarios': funcionarios, 'medicos': medicos, 'recepcionistas': recepcionistas})

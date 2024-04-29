from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from paciente.models import Paciente
from medico.models import Medico
from recept.models import Recepcionista
from itertools import chain
from django.contrib.auth.models import User

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

def dadosPaciente(request, id):
    if request.method == 'post':
        pass
    else:
        paciente = User.objects.get(id=id)
        return render(request, 'paciente_data (prop).html', {'paciente': paciente.paciente})

def dadosFuncionario(request, id):
    if request.method == 'post':
        pass
    else:
        funcionario = User.objects.get(id=id)

        if hasattr(funcionario, 'medico'):
            return render(request, 'funcionario_data (prop).html', {'medico': funcionario.medico})
        elif hasattr(funcionario, 'recepcionista'):
            return render(request, 'funcionario_data (prop).html', {'recepcionista': funcionario.recepcionista})

def addPaciente(request):
    return render(request, 'add_paciente.html')

def addFuncionario(request):
    return render(request, 'add_funcionario.html')

def deletePaciente(request, id):
    paciente = User.objects.get(id=id)
    if request.method == 'POST':
        paciente.delete()
        return redirect(mostrarPacientes)
    else:
        return render(request, 'delete_paciente.html', {'recepcionista': paciente.paciente})

def deleteFuncionario(request, id):
    funcionario = User.objects.get(id=id)
    if request.method == 'POST':
        funcionario.delete()
        return redirect(mostrarFuncionarios)
    else:
        if hasattr(funcionario, 'medico'):
            return render(request, 'delete_funcionario.html', {'medico': funcionario.medico})
        elif hasattr(funcionario, 'recepcionista'):
            return render(request, 'delete_funcionario.html', {'recepcionista': funcionario.recepcionista})
        
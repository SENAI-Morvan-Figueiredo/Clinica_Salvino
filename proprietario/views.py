from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from paciente.models import Paciente
from paciente.forms import CadPaciente
from medico.models import Medico, Especialidade
from medico.forms import CadMedico
from recept.models import Recepcionista
from recept.forms import CadRecep
from itertools import chain
from django.contrib.auth.models import User
from django.contrib import messages

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
        especialidades = Especialidade.objects.all()

        if hasattr(funcionario, 'medico'):
            return render(request, 'medico_data (prop).html', {'medico': funcionario.medico, 'especialidades': especialidades})
        elif hasattr(funcionario, 'recepcionista'):
            return render(request, 'recepcionista_data (prop).html', {'recepcionista': funcionario.recepcionista})

def addPaciente(request):
    if request.method == 'POST':
        paciente_form = CadPaciente(request.POST)
        if paciente_form.is_valid():
            user = User.objects.create_user(
                username=request.POST['username'],
                password=request.POST['password'],
                email=request.POST['username'],
            )
            new_paciente = paciente_form.save(commit=False)
            new_paciente.user = user
            new_paciente.save()
            messages.success(request, 'Paciente Cadastrado com Sucesso!')
            return redirect('adicionar_pacientes')
        else:
            messages.error(request, f"Formulário de cadastro inválido: {paciente_form.errors}")
            return redirect('adicionar_pacientes')
        
    else:
        return render(request, 'add_paciente.html')

def addFuncionario(request):
    if request.method == 'POST':
        tipo = request.POST['tipo_funcionario']
        if tipo == 'recepcionista':
            return redirect('adicionar_recep')
        elif tipo == 'medico':
            return redirect('adicionar_medico')
    else:
        return render(request, 'add_funcionario.html')

def addRecep(request):
    if request.method == 'POST':
        recepcionista_form = CadRecep(request.POST)
        if recepcionista_form.is_valid():
            user = User.objects.create_superuser(
                username=request.POST['username'],
                password=request.POST['password'],
                email=request.POST['username'],
            )
            new_recep = recepcionista_form.save(commit=False)
            new_recep.user = user
            new_recep.save()
            messages.success(request, 'Recepcionista Cadastrado com Sucesso!')
            return redirect('adicionar_funcionarios')
        else:
            messages.error(request, f"Formulário de cadastro inválido: {recepcionista_form.errors}")
            return redirect('adicionar_funcionarios')     
    else: 
        return render(request, 'add_recepcionista.html')
    
def addMecico(request):
    if request.method == 'POST':
        medico_form = CadMedico(request.POST)
        if medico_form.is_valid():
            user = User.objects.create_user(
                username= request.POST['username'],
                password=request.POST['password'],
                email=request.POST['username']
            )
            new_medico = medico_form.save(commit=False)
            new_medico.user = user
            print(new_medico)
            new_medico.save()
            messages.success(request, 'Médico Cadastrado com Sucesso!')
            return redirect('adicionar_funcionarios')
        else:
            messages.error(request, f"Formulário de cadastro inválido: {medico_form.errors}")
            return redirect('adicionar_funcionarios')
    else: 
        especialidades = Especialidade.objects.all()
        return render(request, 'add_medico.html', {'especialidades': especialidades}) 

def deletePaciente(request, id):
    paciente = User.objects.get(id=id)
    if request.method == 'POST':
        paciente.delete()
        return redirect('pacientes')
    else:
        return render(request, 'delete_paciente.html', {'paciente': paciente.paciente})

def deleteFuncionario(request, id):
    funcionario = User.objects.get(id=id)
    if request.method == 'POST':
        funcionario.delete()
        return redirect('funcionarios')
    else:
        if hasattr(funcionario, 'medico'):
            return render(request, 'delete_funcionario.html', {'medico': funcionario.medico})
        elif hasattr(funcionario, 'recepcionista'):
            return render(request, 'delete_funcionario.html', {'recepcionista': funcionario.recepcionista})
        
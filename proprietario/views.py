from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from paciente.models import Paciente
from paciente.forms import CadPaciente
from medico.models import Medico, Especialidade
from medico.forms import CadMedico, CadEspecialidade
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

def mostrarEspecialidades(request):
    especialidades = Especialidade.objects.all()
    return render(request, 'especialidades_list.html', {'especialidades': especialidades})

def dadosPaciente(request, id):
    user = User.objects.get(id=id)
    paciente = Paciente.objects.get(user=user)
    if request.method == 'POST':
        edit_paciente_form = CadPaciente(request.POST, instance=paciente)
        if edit_paciente_form.is_valid():
            edit_paciente_form.save(commit=False)
            paciente.save()
            messages.success(request, 'Dados do paciente editados com Sucesso!')
            return redirect('paciente', id=id)
        else:
            messages.error(request, f"Edição inválida: {edit_paciente_form.errors}")
            return redirect('paciente', id=id)
    else:
        return render(request, 'paciente_data (prop).html', {'paciente': paciente})

def dadosFuncionario(request, id):
    user = User.objects.get(id=id)
    if request.method == 'POST':
        if hasattr(user, 'medico'):
            medico = Medico.objects.get(user=user)
            edit_medico_form = CadMedico(request.POST, instance=medico)
            if edit_medico_form.is_valid():
                edit_medico_form.save(commit=False)
                medico.save()
                messages.success(request, 'Dados do médico editados com Sucesso!')
                return redirect('funcionario', id=id)
            else:
                messages.error(request, f"Edição inválida: {edit_medico_form.errors}")
                return redirect('funcionario', id=id)
        elif hasattr(user, 'recepcionista'):
            recepcionista = Recepcionista.objects.get(user=user)
            edit_recepcionista_form = CadRecep(request.POST, instance=recepcionista)
            if edit_recepcionista_form.is_valid():
                edit_recepcionista_form.save(commit=False)
                recepcionista.save()
                messages.success(request, 'Dados do recepcionista editados com Sucesso!')
                return redirect('funcionario', id=id)
            else:
                messages.error(request, f"Edição inválida: {edit_recepcionista_form.errors}")
                return redirect('funcionario', id=id)
    else:
        especialidades = Especialidade.objects.all()
        if hasattr(user, 'medico'):
            return render(request, 'medico_data (prop).html', {'medico': user.medico, 'especialidades': especialidades})
        elif hasattr(user, 'recepcionista'):
            return render(request, 'recepcionista_data (prop).html', {'recepcionista': user.recepcionista})
        
def dadosEspecialidade(request, id):
    especialidade = Especialidade.objects.get(id=id)
    if request.method == 'POST':
        edit_esp_form = CadEspecialidade(request.POST, instance=especialidade)
        if edit_esp_form.is_valid():
            edit_esp_form.save(commit=False)
            especialidade.save()
            messages.success(request, 'Dados da especialidade editados com Sucesso!')
            return redirect('especialidade', id=id)
        else:
            messages.error(request, f"Edição inválida: {edit_esp_form.errors}")
            return redirect('especialidade', id=id)
    else:
        return render(request, 'especialidade.html', {'especialidade': especialidade})

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
    
def addMedico(request):
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
    
def addEspecialidade(request):
    if request.method == 'POST':
        esp_form = CadEspecialidade(request.POST)
        if esp_form.is_valid():
            new_especialidade = esp_form.save(commit=False)
            new_especialidade.save()
            messages.success(request, 'Especialidade Cadastrada com Sucesso!')
            return redirect('adicionar_especialidade')
        else:
            messages.error(request, f"Formulário de cadastro inválido: {esp_form.errors}")
            return redirect('adicionar_especialidade')
    else:
        return render(request, 'add_especialidade.html')

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
        
def deleteEspecialidade(request, id):
    especialidade = Especialidade.objects.get(id=id)
    if request.method == 'POST':
        especialidade.delete()
        return redirect('especialidades')
    else:
        return render(request, 'delete_especialidade.html', {'especialidade': especialidade})

        
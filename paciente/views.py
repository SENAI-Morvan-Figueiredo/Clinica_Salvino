import logging
from django.shortcuts import render, redirect
from .forms import CadPaciente
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required

logger = logging.getLogger(__name__)

# Create your views here.
def register(request):
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
            messages.success(request, 'Usuário Cadastrado com Sucesso!')
            return redirect('cadastro')
        else:
            messages.error(request, f"Formulário de cadastro inválido: {paciente_form.errors}")
            return redirect('cadastro')
    else:
        return render(request, 'register.html')

@login_required   
def pacienteBoard(request):
    paciente = request.user.paciente
    return render(request, 'paciente.html', {'paciente': paciente})

def contaPaciente(request):
    paciente = request.user.paciente
    return render(request, 'myaccount_paciente.html', {'paciente': paciente})

def pagamento(request):
    paciente = request.user.paciente
    return render(request, 'pagamento.html', {'paciente': paciente}) 

def agendamento(request):
    paciente = request.user.paciente
    return render(request, 'agendamento(paciente).html', {'paciente': paciente}) 

def add_cartao(request):
    paciente = request.user.paciente
    return render(request, 'add_cartao(paciente).html', {'paciente': paciente}) 

def add_convenio(request):
    paciente = request.user.paciente
    return render(request, 'add_convenio(paciente).html', {'paciente': paciente}) 
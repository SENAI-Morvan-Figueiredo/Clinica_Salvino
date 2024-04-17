import logging
from django.shortcuts import render, redirect
from .forms import CadPaciente
from django.contrib.auth.models import User
from django.contrib import messages

logger = logging.getLogger(__name__)

# Create your views here.
def register(request):
    if request.method == 'POST':
        paciente_form = CadPaciente(request.POST)
        if paciente_form.is_valid():
            user = User.objects.create_user(
                username=request.POST['username'],
                password=request.POST['password'],
                email=request.POST['email'],
            )
            new_paciente = paciente_form.save(commit=False)
            new_paciente.user = user
            new_paciente.save()
            messages.success(request, 'Usuário Cadastrado com Sucesso!')
            return redirect('cadastro')
        else:
            messages.error("Formulário de cadastro inválido: %s", paciente_form.errors)
            return redirect('cadastro')
    else:
        return render(request, 'register.html')
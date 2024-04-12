import logging
from django.shortcuts import render, redirect, HttpResponse
from .forms import CadPaciente
from .models import Paciente


logger = logging.getLogger(__name__)

# Create your views here.
def register(request):
    if request.method == 'POST':
        paciente_form = CadPaciente(request.POST)
        if paciente_form.is_valid():
            new_paciente = paciente_form.save(commit=False)
            new_paciente.save()
            logger.info("Paciente cadastrado com sucesso.")
            return redirect('cadastro')
        else:
            logger.error("Formulário de cadastro inválido: %s", paciente_form.errors)
            return redirect('cadastro')
    else:
        return render(request, 'register.html')
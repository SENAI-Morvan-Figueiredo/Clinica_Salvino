import logging
from django.shortcuts import render, redirect, HttpResponse
from .forms import CadPaciente
from django.contrib.auth.models import User

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
            return redirect('cadastro')
        else:
            logger.error("Formulário de cadastro inválido: %s", paciente_form.errors)
            return redirect('cadastro')
    else:
        return render(request, 'register.html')
    
def card(request):
    return render(request, 'card.html')

def paciente(request):
    return render(request, 'paciente.html')

def payment(request):
    return render(request, 'payment.html')

def nutricionista(request):
    return render(request, 'nutricionista.html')
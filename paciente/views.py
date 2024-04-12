from django.shortcuts import render, redirect
from .forms import CadPaciente
from .models import Paciente

# Create your views here.
def register(request):
    if request.method == 'POST':
        paciente_form = CadPaciente(request.POST)
        if paciente_form.is_valid():
            new_paciente = paciente_form.save(commit=False)
            new_paciente.save()
            return redirect('cadastro')
        else:
            return redirect('cadastro')
    else:
        return render(request, 'register.html')
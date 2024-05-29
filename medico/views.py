from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from paciente.models import Paciente, Consulta, CadCartao, CadConvenio, AnexoConsulta, Documentos, Prontuario, Boleto, Pagamento
from paciente.forms import CadPaciente, AgendaConsulta, FormCartao, FormConvenio, AnexoForm, ProntuarioForm, PagamentoCard, PagamentoConv, PagamentoPix


# Create your views here.
@login_required 
def medBoard(request):
    medico = request.user.medico
    return render(request, 'medico.html', {'medico': medico})
    
def contaMedico(request):
    medico = request.user.medico
    return render(request, 'myaccount_medico.html', {'medico': medico})

def mostrarPacientes(request):
    medico = request.user.medico
    pacientes = Paciente.objects.all()
    return render(request, 'pacientes_list(med).html', {'medico': medico, 'pacientes': pacientes})

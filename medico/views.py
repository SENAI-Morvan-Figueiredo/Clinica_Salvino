from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from paciente.models import Paciente, Consulta, CadCartao, CadConvenio, AnexoConsulta, Documentos, Prontuario, Boleto, Pagamento
from paciente.forms import CadPaciente, AgendaConsulta, FormCartao, FormConvenio, AnexoForm, ProntuarioForm, PagamentoCard, PagamentoConv, PagamentoPix
from collections import defaultdict
from django.contrib.auth.models import User
from django.contrib import messages
from datetime import date

# Create your views here.
@login_required 
def medBoard(request):
    medico = request.user.medico
    consultas = Consulta.objects.filter(medico=medico, status_consulta = 'Ficha Aberta')
    return render(request, 'medico.html', {'medico': medico, 'consultas': consultas})
    
def contaMedico(request):
    medico = request.user.medico
    return render(request, 'myaccount_medico.html', {'medico': medico})

def mostrarPacientes(request):
    medico = request.user.medico
    consultas = Consulta.objects.filter(medico=medico)
    pacientes = set(consulta.paciente for consulta in consultas)

    return render(request, 'pacientes_list(med).html', {'medico': medico, 'pacientes': pacientes})

def dadosPaciente(request, id):
    medico = request.user.medico
    user = User.objects.get(id=id)
    paciente = Paciente.objects.get(user=user)
    return render(request, 'paciente_data (med).html', {'medico': medico, 'paciente': paciente})


def document_list(request, id):
    # Agrupar documentos por data
    medico = request.user.medico
    list_documents = defaultdict(list)
    user = User.objects.get(id=id)
    paciente = Paciente.objects.get(user=user)
    try:
        prontuario = Prontuario.objects.get(paciente=paciente)
        if prontuario:
            documents = Documentos.objects.filter(prontuario=prontuario)
            if documents:
                for document in documents.order_by('data'):
                    list_documents[document.data].append(document)

                return render(request, 'prontuario (med).html', {'medico': medico,'paciente':paciente,'prontuario': prontuario, 'list_documents': list_documents.items()})
            else:
                list_documents = ''
                return render(request, 'prontuario (med).html', {'medico': medico, 'paciente':paciente,'prontuario': prontuario, 'list_documents': list_documents})
    except:
        prontuario = ''
        return render(request, 'prontuario (med).html', {'medico': medico, 'paciente':paciente, 'prontuario': prontuario, 'listdocumentos': ''})
    
def init_prontuario(request, id):
    medico = request.user.medico
    user = User.objects.get(id=id)
    paciente = Paciente.objects.get(user=user)
    if request.method == 'POST':
        prontuario_form = ProntuarioForm(request.POST)
        if prontuario_form.is_valid():
            new_prontuario = prontuario_form.save(commit=False)
            new_prontuario.paciente = paciente
            new_prontuario.save()
            show_message = request.session.pop('show_message', False)
            messages.success(request, 'Convênio do paciente cadastrado com Sucesso!')
            return redirect('prontuario_med', id)
        else:
            show_message = request.session.pop('show_message', False)
            messages.error(request, f"Formulário de cartão inválido: {prontuario_form.errors}")
            return redirect('prontuario_med', id)   
    else:
        show_message = request.session.pop('show_message', False)
        return render(request, 'init_prontuario (med).html', {'medico': medico, 'paciente': paciente, 'message_view': show_message})

def info_prontuario(request, id):
    medico = request.user.medico
    user = User.objects.get(id=id)
    paciente = Paciente.objects.get(user=user)
    prontuario = Prontuario.objects.get(paciente=paciente)
    return render(request, 'info_prontuario (med).html', {'medico': medico, 'paciente': paciente, 'prontuario': prontuario})

def mostrarConsultas(request):
    medico = request.user.medico
    consultas = Consulta.objects.filter(medico=medico).order_by('status_consulta')
    data = date.today()
    return render(request, 'consultas (med).html', {'medico': medico, 'consultas': consultas, 'data': data})

def concluirConsulta(request, id):
    medico = request.user.medico
    consulta = Consulta.objects.get(id=id)
    if request.method == 'POST':
        consulta.status_consulta = 'Concluida'
        consulta.save()
        return redirect('consultas')
    else:
        return render(request, 'concluir_consulta.html', {'medico': medico, 'consulta': consulta})
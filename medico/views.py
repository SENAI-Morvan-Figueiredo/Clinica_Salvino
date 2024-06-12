from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from paciente.models import Paciente, Consulta, Documentos, Prontuario, Encaminhamento, Bioimpedância, AnexoConsulta
from paciente.forms import ProntuarioForm, addDocumento, addEncaminhamento, addBioimpedância
from collections import defaultdict
from django.contrib.auth.models import User
from django.contrib import messages
from datetime import date
from itertools import chain
from clinica_salvino.decorators import group_required

# Create your views here.
@group_required('Medico')
def medBoard(request):
    medico = request.user.medico
    consultas = Consulta.objects.filter(medico=medico, status_consulta = 'Ficha Aberta')
    return render(request, 'medico.html', {'medico': medico, 'consultas': consultas})

@group_required('Medico')
@login_required   
def contaMedico(request):
    medico = request.user.medico
    return render(request, 'myaccount_medico.html', {'medico': medico})

@group_required('Medico')
@login_required 
def mostrarPacientes(request):
    medico = request.user.medico
    consultas = Consulta.objects.filter(medico=medico)
    pacientes = set(consulta.paciente for consulta in consultas)

    return render(request, 'pacientes_list(med).html', {'medico': medico, 'pacientes': pacientes})

@group_required('Medico')
@login_required 
def dadosPaciente(request, id):
    medico = request.user.medico
    user = User.objects.get(id=id)
    paciente = Paciente.objects.get(user=user)
    return render(request, 'paciente_data (med).html', {'medico': medico, 'paciente': paciente})

@group_required('Medico')
@login_required 
def document_list(request, id):
    # Agrupar documentos por data
    medico = request.user.medico
    list_documents = defaultdict(list)
    user = User.objects.get(id=id)
    paciente = Paciente.objects.get(user=user)
    try:
        prontuario = Prontuario.objects.get(paciente=paciente)
        if prontuario:
            documentos = Documentos.objects.filter(prontuario=prontuario).order_by('data')
            encaminhamentos = Encaminhamento.objects.filter(prontuario=prontuario).order_by('data')
            bioimpedancia = Bioimpedância.objects.filter(prontuario=prontuario).order_by('data')
            consultas = Consulta.objects.filter(paciente = paciente)
            anexos = []

            for consulta in consultas:
                arquivos = AnexoConsulta.objects.filter(consulta=consulta)
                for arquivo in arquivos:
                    arquivo.data = consulta.data
                    anexos.append(arquivo)

            documents_list = list(chain(documentos, encaminhamentos, bioimpedancia, anexos))
            if documents_list:
                documents_list.sort(key=lambda x: x.data)
                for document in documents_list:
                    list_documents[document.data].append(document)

                return render(request, 'prontuario (med).html', {'medico': medico,'paciente':paciente,'prontuario': prontuario, 'list_documents': list_documents.items(), 'documentos' : documentos, 'encaminhamentos': encaminhamentos, 'bioimpedancia': bioimpedancia, 'anexos': anexos})
            else:
                list_documents = ''
                return render(request, 'prontuario (med).html', {'medico': medico, 'paciente':paciente,'prontuario': prontuario, 'list_documents': list_documents})
    except:
        prontuario = ''
        return render(request, 'prontuario (med).html', {'medico': medico, 'paciente':paciente, 'prontuario': prontuario, 'listdocumentos': ''})

@group_required('Medico')
@login_required    
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
            return redirect('prontuario_med', id)
        else:
            show_message = request.session.pop('show_message', False)
            messages.error(request, f"Formulário de cartão inválido: {prontuario_form.errors}")
            return redirect('prontuario_med', id)   
    else:
        show_message = request.session.pop('show_message', False)
        return render(request, 'init_prontuario (med).html', {'medico': medico, 'paciente': paciente, 'message_view': show_message})

@group_required('Medico')
@login_required 
def info_prontuario(request, id):
    medico = request.user.medico
    user = User.objects.get(id=id)
    paciente = Paciente.objects.get(user=user)
    prontuario = Prontuario.objects.get(paciente=paciente)
    if request.method == 'POST':
        edit_prontuario_form = ProntuarioForm(request.POST, instance=prontuario)
        if edit_prontuario_form.is_valid():
            edit_prontuario_form.save(commit=False)
            prontuario.save()
            return redirect('prontuario_med', id)
        else:
            request.session['show_message'] = True 
            messages.error(request, f"Edição inválida: {edit_prontuario_form.errors}")
            return redirect('info_prontuario_med', id)
    else:
        return render(request, 'info_prontuario (med).html', {'medico': medico, 'paciente': paciente, 'prontuario': prontuario})

@group_required('Medico')
@login_required 
def mostrarConsultas(request):
    medico = request.user.medico
    consultas = Consulta.objects.filter(medico=medico).order_by('status_consulta')
    data = date.today()
    return render(request, 'consultas (med).html', {'medico': medico, 'consultas': consultas, 'data': data})

@group_required('Medico')
@login_required 
def concluirConsulta(request, id):
    medico = request.user.medico
    consulta = Consulta.objects.get(id=id)
    if request.method == 'POST':
        consulta.status_consulta = 'Concluida'
        consulta.save()
        return redirect('consultas')
    else:
        return render(request, 'concluir_consulta.html', {'medico': medico, 'consulta': consulta})

@group_required('Medico')
@login_required     
def addDocument(request, id):
    medico = request.user.medico
    user = User.objects.get(id=id)
    paciente = Paciente.objects.get(user=user)
    prontuario = Prontuario.objects.get(paciente=paciente)
    if request.method == "POST":
        doc_form = addDocumento(request.POST, request.FILES)
        if doc_form.is_valid():
            new_doc = doc_form.save(commit=False)
            new_doc.prontuario = prontuario
            new_doc.medico = medico
            new_doc.save()
            return redirect('prontuario_med', id) 
        else:
            messages.error(request, f"Erro ao salvar o arquivo: {doc_form.errors}")
            request.session['show_message'] = True
            return redirect('add_doc_med', id) 
    else:
        show_message = request.session.pop('show_message', False)
        return render(request, 'add_documento (med).html', {'medico': medico, 'prontuario': prontuario, 'message_view': show_message})

@group_required('Medico')
@login_required     
def document(request, id):
    medico = request.user.medico
    documento = Documentos.objects.get(id=id)
    
    return render(request, 'documento (med).html', {'medico': medico, 'documento': documento})

@group_required('Medico')
@login_required 
def addEncaminha(request, id):
    medico = request.user.medico
    user = User.objects.get(id=id)
    paciente = Paciente.objects.get(user=user)
    prontuario = Prontuario.objects.get(paciente=paciente)
    if request.method == "POST":
        doc_form = addEncaminhamento(request.POST, request.FILES)
        if doc_form.is_valid():
            new_doc = doc_form.save(commit=False)
            new_doc.prontuario = prontuario
            new_doc.medico = medico
            new_doc.save()
            return redirect('prontuario_med', id) 
        else:
            messages.error(request, f"Erro ao salvar o arquivo: {doc_form.errors}")
            request.session['show_message'] = True
            return redirect('add_doc_med', id) 
    else:
        show_message = request.session.pop('show_message', False)
        return render(request, 'add_encaminhamento (med).html', {'medico': medico, 'prontuario': prontuario, 'message_view': show_message})

@group_required('Medico')
@login_required 
def encaminha(request, id):
    medico = request.user.medico
    encaminhamento = Encaminhamento.objects.get(id=id)
    
    return render(request, 'encaminhamento (med).html', {'medico': medico, 'encaminhamento': encaminhamento})

@group_required('Medico')
@login_required 
def addBio(request, id):
    medico = request.user.medico
    user = User.objects.get(id=id)
    paciente = Paciente.objects.get(user=user)
    prontuario = Prontuario.objects.get(paciente=paciente)
    if request.method == "POST":
        doc_form = addBioimpedância(request.POST, request.FILES)
        if doc_form.is_valid():
            new_doc = doc_form.save(commit=False)
            new_doc.prontuario = prontuario
            new_doc.medico = medico
            new_doc.save()
            return redirect('prontuario_med', id) 
        else:
            messages.error(request, f"Erro ao salvar o arquivo: {doc_form.errors}")
            request.session['show_message'] = True
            return redirect('add_bio_med', id) 
    else:
        show_message = request.session.pop('show_message', False)
        return render(request, 'add_bioimpedancia (med).html', {'medico': medico, 'prontuario': prontuario, 'message_view': show_message})

@group_required('Medico')
@login_required 
def bio(request, id):
    medico = request.user.medico
    bioimpedancia = Bioimpedância.objects.get(id=id)
    
    return render(request, 'bioimpedancia (med).html', {'medico': medico, 'bioimpedancia': bioimpedancia})

@group_required('Medico')
@login_required 
def delete_en(request, id):
    medico = request.user.medico
    encaminhamento = Encaminhamento.objects.get(id=id)
    if request.method == 'POST':
        encaminhamento.delete()
        return redirect('prontuario_med', encaminhamento.prontuario.paciente.user.id)
    else:
        return render(request, 'delete_encaminhamento (med).html', {'medico': medico, 'encaminhamento': encaminhamento})

@group_required('Medico')
@login_required 
def delete_doc(request, id):
    medico = request.user.medico
    documento = Documentos.objects.get(id=id)
    if request.method == 'POST':
        documento.delete()
        return redirect('prontuario_med', documento.prontuario.paciente.user.id)
    else:
        return render(request, 'delete_documento (med).html', {'medico': medico, 'documento': documento})

@group_required('Medico')
@login_required 
def delete_bio(request, id):
    medico = request.user.medico
    bioimpedancia = Bioimpedância.objects.get(id=id)
    if request.method == 'POST':
        bioimpedancia.delete()
        return redirect('prontuario_med', bioimpedancia.prontuario.paciente.user.id)
    else:
        return render(request, 'delete_bioimpedancia (med).html', {'medico': medico, 'bioimpedancia': bioimpedancia})
    
@group_required('Medico')
@login_required 
def anexo(request, id):
    medico = request.user.medico
    anexo = AnexoConsulta.objects.get(id=id)
    
    return render(request, 'anexo (med).html', {'medico': medico, 'documento': anexo})
    
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from clinica.models import BandeiraCartao, Convenio, PlanoConvenio, Tratamento, Pix
from clinica.forms import CadBandeira, EmpresaConvenio, CadPlano, CadTratamento, CadPix
from paciente.models import Paciente, Consulta, CadCartao, CadConvenio, AnexoConsulta, Documentos, Prontuario, Boleto, Pagamento, Encaminhamento, Bioimpedância
from paciente.forms import CadPaciente, AgendaConsulta, FormCartao, FormConvenio, AnexoForm, ProntuarioForm, PagamentoCard, PagamentoConv, PagamentoPix
from medico.models import Medico, Especialidade
from medico.forms import CadMedico, CadEspecialidade
from recept.models import Recepcionista
from recept.forms import CadRecep
from .models import Proprietario
from .forms import CadProprietario
from itertools import chain
from django.contrib.auth.models import User
from django.contrib import messages
from datetime import date
from collections import defaultdict
from clinica_salvino.decorators import group_required
from django.core.files.storage import FileSystemStorage
from django.core.files import File
from django.conf import settings
import os
import tempfile

# Create your views here.
@group_required('Proprietario')
@login_required 
def proprietyBoard(request):
    proprietario = request.user.proprietario
    return render(request, 'proprietario.html', {'proprietario': proprietario})

@group_required('Proprietario')
@login_required 
def contaProprietario(request):
    user = request.user
    proprietario = Proprietario.objects.get(user=user)
    if request.method == 'POST':
        edit_prop_form = CadProprietario(request.POST, instance=proprietario)
        if edit_prop_form.is_valid():
            edit_prop_form.save(commit=False)
            proprietario.save()
            request.session['show_message'] = True 
            messages.success(request, 'Seus dados foram editados com Sucesso!')
            return redirect('conta_proprietario')
        else:
            request.session['show_message'] = True 
            messages.error(request, f"Edição inválida: {edit_prop_form.errors}")
            return redirect('conta_proprietario')
    else:
        show_message = request.session.pop('show_message', False)
        return render(request, 'myaccount_proprietario.html', {'proprietario': proprietario, 'message_view': show_message})

@group_required('Proprietario')
@login_required 
def mostrarPacientes(request):
    proprietario = request.user.proprietario
    pacientes = Paciente.objects.all()
    return render(request, 'pacientes_list (prop).html', {'proprietario': proprietario, 'pacientes': pacientes})

@group_required('Proprietario')
@login_required 
def mostrarFuncionarios(request):
    proprietario = request.user.proprietario
    medicos = Medico.objects.all()
    recepcionistas = Recepcionista.objects.all()

    funcionarios = list(chain(medicos, recepcionistas))

    return render(request, 'funcionarios_list (prop).html', {'proprietario': proprietario, 'funcionarios': funcionarios, 'medicos': medicos, 'recepcionistas': recepcionistas})

@group_required('Proprietario')
@login_required 
def mostrarEspecialidades(request):
    proprietario = request.user.proprietario
    especialidades = Especialidade.objects.all()
    return render(request, 'especialidades_list.html', {'proprietario': proprietario, 'especialidades': especialidades})

@group_required('Proprietario')
@login_required 
def dadosPaciente(request, id):
    proprietario = request.user.proprietario
    user = User.objects.get(id=id)
    paciente = Paciente.objects.get(user=user)
    if request.method == 'POST':
        edit_paciente_form = CadPaciente(request.POST, instance=paciente)
        if edit_paciente_form.is_valid():
            edit_paciente_form.save(commit=False)
            paciente.save()
            request.session['show_message'] = True 
            messages.success(request, 'Dados do paciente editados com Sucesso!')
            return redirect('paciente', id=id)
        else:
            request.session['show_message'] = True 
            messages.error(request, f"Edição inválida: {edit_paciente_form.errors}")
            return redirect('paciente', id=id)
    else:
        show_message = request.session.pop('show_message', False)
        return render(request, 'paciente_data (prop).html', {'proprietario': proprietario, 'paciente': paciente, 'message_view': show_message})

@group_required('Proprietario')
@login_required 
def dadosFuncionario(request, id):
    proprietario = request.user.proprietario
    user = User.objects.get(id=id)
    if request.method == 'POST':
        if hasattr(user, 'medico'):
            medico = Medico.objects.get(user=user)
            edit_medico_form = CadMedico(request.POST, instance=medico)
            if edit_medico_form.is_valid():
                edit_medico_form.save(commit=False)
                medico.save()
                request.session['show_message'] = True 
                messages.success(request, 'Dados do médico editados com Sucesso!')
                return redirect('funcionario', id=id)
            else:
                request.session['show_message'] = True 
                messages.error(request, f"Edição inválida: {edit_medico_form.errors}")
                return redirect('funcionario', id=id)
        elif hasattr(user, 'recepcionista'):
            recepcionista = Recepcionista.objects.get(user=user)
            edit_recepcionista_form = CadRecep(request.POST, instance=recepcionista)
            if edit_recepcionista_form.is_valid():
                edit_recepcionista_form.save(commit=False)
                recepcionista.save()
                request.session['show_message'] = True 
                messages.success(request, 'Dados do recepcionista editados com Sucesso!')
                return redirect('funcionario', id=id)
            else:
                request.session['show_message'] = True 
                messages.error(request, f"Edição inválida: {edit_recepcionista_form.errors}")
                return redirect('funcionario', id=id)
    else:
        show_message = request.session.pop('show_message', False)
        especialidades = Especialidade.objects.all()
        if hasattr(user, 'medico'):
            return render(request, 'medico_data (prop).html', {'proprietario': proprietario, 'medico': user.medico, 'especialidades': especialidades, 'message_view': show_message})
        elif hasattr(user, 'recepcionista'):
            return render(request, 'recepcionista_data (prop).html', {'proprietario': proprietario, 'recepcionista': user.recepcionista, 'message_view': show_message})

@group_required('Proprietario')
@login_required       
def dadosEspecialidade(request, id):
    proprietario = request.user.proprietario
    especialidade = Especialidade.objects.get(id=id)
    if request.method == 'POST':
        edit_esp_form = CadEspecialidade(request.POST, instance=especialidade)
        if edit_esp_form.is_valid():
            edit_esp_form.save(commit=False)
            especialidade.save()
            request.session['show_message'] = True 
            messages.success(request, 'Dados da especialidade editados com Sucesso!')
            return redirect('especialidade', id=id)
        else:
            request.session['show_message'] = True 
            messages.error(request, f"Edição inválida: {edit_esp_form.errors}")
            return redirect('especialidade', id=id)
    else:
        show_message = request.session.pop('show_message', False)
        return render(request, 'especialidade.html', {'proprietario': proprietario, 'especialidade': especialidade, 'message_view': show_message})

@group_required('Proprietario')
@login_required 
def addPaciente(request):
    proprietario = request.user.proprietario
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
            request.session['show_message'] = True 
            return redirect('adicionar_pacientes')
        else:
            messages.error(request, f"Formulário de cadastro inválido: {paciente_form.errors}")
            request.session['show_message'] = True 
            return redirect('adicionar_pacientes')
        
    else:
        show_message = request.session.pop('show_message', False)
        return render(request, 'add_paciente (prop).html', {'proprietario': proprietario,'message_view': show_message})

@group_required('Proprietario')
@login_required 
def addFuncionario(request):
    proprietario = request.user.proprietario
    if request.method == 'POST':
        tipo = request.POST['tipo_funcionario']
        if tipo == 'recepcionista':
            return redirect('adicionar_recep')
        elif tipo == 'medico':
            return redirect('adicionar_medico')
    else:
        show_message = request.session.pop('show_message', False)
        return render(request, 'add_funcionario.html', {'proprietario': proprietario,'message_view': show_message})

@group_required('Proprietario')
@login_required 
def addRecep(request):
    proprietario = request.user.proprietario
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
            request.session['show_message'] = True 
            return redirect('adicionar_funcionarios')
        else:
            messages.error(request, f"Formulário de cadastro inválido: {recepcionista_form.errors}")
            request.session['show_message'] = True 
            return redirect('adicionar_funcionarios')     
    else:
        request.session['show_message'] = False
        return render(request, 'add_recepcionista.html', {'proprietario': proprietario})

@group_required('Proprietario')
@login_required     
def addMedico(request):
    proprietario = request.user.proprietario
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
            new_medico.save()
            messages.success(request, 'Médico Cadastrado com Sucesso!')
            request.session['show_message'] = True  
            return redirect('adicionar_funcionarios')
        else:
            messages.error(request, f"Formulário de cadastro inválido: {medico_form.errors}")
            request.session['show_message'] = True 
            return redirect('adicionar_funcionarios')
    else: 
        especialidades = Especialidade.objects.all()
        request.session['show_message'] = False
        return render(request, 'add_medico.html', {'proprietario': proprietario, 'especialidades': especialidades}) 

@group_required('Proprietario')
@login_required 
def addEspecialidade(request):
    proprietario = request.user.proprietario
    if request.method == 'POST':
        esp_form = CadEspecialidade(request.POST)
        if esp_form.is_valid():
            new_especialidade = esp_form.save(commit=False)
            new_especialidade.save()
            messages.success(request, 'Especialidade Cadastrada com Sucesso!')
            request.session['show_message'] = True 
            return redirect('adicionar_especialidade')
        else:
            messages.error(request, f"Formulário de cadastro inválido: {esp_form.errors}")
            request.session['show_message'] = True 
            return redirect('adicionar_especialidade')
    else:
        show_message = request.session.pop('show_message', False)
        return render(request, 'add_especialidade.html', {'proprietario': proprietario, 'message_view': show_message})

@group_required('Proprietario')
@login_required 
def deletePaciente(request, id):
    proprietario = request.user.proprietario
    paciente = User.objects.get(id=id)
    if request.method == 'POST':
        paciente.delete()
        return redirect('pacientes')
    else:
        return render(request, 'delete_paciente (prop).html', {'proprietario': proprietario, 'paciente': paciente.paciente})

@group_required('Proprietario')
@login_required 
def deleteFuncionario(request, id):
    proprietario = request.user.proprietario
    funcionario = User.objects.get(id=id)
    if request.method == 'POST':
        funcionario.delete()
        return redirect('funcionarios')
    else:
        if hasattr(funcionario, 'medico'):
            return render(request, 'delete_funcionario.html', {'proprietario': proprietario, 'medico': funcionario.medico})
        elif hasattr(funcionario, 'recepcionista'):
            return render(request, 'delete_funcionario.html', {'proprietario': proprietario, 'recepcionista': funcionario.recepcionista})

@group_required('Proprietario')
@login_required       
def deleteEspecialidade(request, id):
    proprietario = request.user.proprietario
    especialidade = Especialidade.objects.get(id=id)
    if request.method == 'POST':
        especialidade.delete()
        return redirect('especialidades')
    else:
        return render(request, 'delete_especialidade.html', {'proprietario': proprietario, 'especialidade': especialidade})

@group_required('Proprietario')
@login_required 
def mostrarConsultas(request):
    proprietario = request.user.proprietario
    consultas = Consulta.objects.all().order_by('status_consulta')
    return render(request, 'consultas (prop).html', {'proprietario': proprietario, 'consultas': consultas})

@group_required('Proprietario')
@login_required 
def marcarConsulta(request):
    proprietario = request.user.proprietario
    especialidade = Especialidade.objects.all()
    if request.method == 'POST':
        atendimento_form = AgendaConsulta(request.POST, request.FILES)
        anexo_form = AnexoForm(request.POST, request.FILES)
        if atendimento_form.is_valid() and anexo_form.is_valid():
            atendimento_data = atendimento_form.cleaned_data
            anexo_files = request.FILES.getlist('arquivos')
            
            # Salvando os arquivos temporariamente
            temp_dir = settings.TEMP_DIR
            saved_files = []
            for arquivo in anexo_files:
                fs = FileSystemStorage(location=temp_dir)
                filename = fs.save(arquivo.name, arquivo)
                saved_files.append(fs.path(filename))

            serializable_atendimento_data = {
                'paciente_id': atendimento_data['paciente'].id,
                'tipo_consulta': atendimento_data['tipo_consulta'],
                'medico_id': atendimento_data['medico'].id,
                'data': atendimento_data['data'].isoformat(),
                'hora': atendimento_data['hora'].isoformat(),
                'especialidade_id': atendimento_data['especialidade'].id,
            }

            request.session['atendimento_data'] = serializable_atendimento_data
            request.session['anexo_files'] = saved_files
            tratamentos = Tratamento.objects.all()
            if tratamentos:
                return redirect('pay_prop')
            else:
                messages.error(request, f"Não há tratamentos cadastrados")
                request.session['show_message'] = True 
                return redirect('agendamento_prop')
        else:
            messages.error(request, f"Agendamento inválido: {atendimento_form.errors}")
            request.session['show_message'] = True 
            return redirect('agendamento_prop')
    else:
        pacientes = Paciente.objects.all()
        medicos = Medico.objects.all()
        show_message = request.session.pop('show_message', False)
        return render(request, 'agendamento (prop).html', {'proprietario': proprietario, 'medicos': medicos, 'pacientes': pacientes, 'especialidades': especialidade,'message_view': show_message})

@group_required('Proprietario')
@login_required  
def cancelarConsulta(request, id):
    proprietario = request.user.proprietario
    consulta = Consulta.objects.get(id=id)
    pagamento = Pagamento.objects.get(consulta=consulta)
    if request.method == 'POST':
        consulta.status_consulta = 'Cancelada'
        pagamento.status_pagamento = 'Cancelado'
        pagamento.save()
        consulta.save()
        return redirect('consultas')
    else:
        return render(request, 'cancelar_consulta (prop).html', {'proprietario': proprietario, 'consulta': consulta})

@group_required('Proprietario')
@login_required   
def mostrarBandeiras(request):
    proprietario = request.user.proprietario
    bandeiras = BandeiraCartao.objects.all()

    return render(request, 'bandeiras_cartao_list.html', {'proprietario': proprietario, 'bandeiras': bandeiras})

@group_required('Proprietario')
@login_required    
def adicionarBandeira(request):
    proprietario = request.user.proprietario
    if request.method == 'POST':
        bandeira = CadBandeira(request.POST)
        if bandeira.is_valid():
            new_bandeira = bandeira.save(commit=False)
            new_bandeira.save()
            messages.success(request, 'Bandeira cadastrada com Sucesso!')
            request.session['show_message'] = True 
            return redirect('adicionar_bandeira')
        else:
            messages.error(request, f"Cadastro de bandeira inválido: {bandeira.errors}")
            request.session['show_message'] = True 
            return redirect('adicionar_bandeira')
    else:
        show_message = request.session.pop('show_message', False)
        return render(request, 'add_bandeira_cartao.html', {'proprietario': proprietario,'message_view': show_message})

@group_required('Proprietario')
@login_required    
def deleteBandeira(request, id):
    proprietario = request.user.proprietario
    bandeira = BandeiraCartao.objects.get(id=id)
    if request.method == 'POST':
        bandeira.delete()
        return redirect('bandeiras')
    else:
        return render(request, 'delete_bandeira.html', {'proprietario': proprietario, 'bandeira': bandeira})

@group_required('Proprietario')
@login_required  
def mostrarCartoes(request, id):
    proprietario = request.user.proprietario
    user = User.objects.get(id=id)
    paciente = Paciente.objects.get(user=user)
    try:
        cartoes = CadCartao.objects.filter(paciente=paciente)
    except:
        cartoes = ''
    finally:
        return render(request, 'cartoes_list (prop).html', {'proprietario': proprietario, 'paciente': paciente, 'cartoes': cartoes})

@group_required('Proprietario')
@login_required 
def adicionarCartoes(request,id):
    proprietario = request.user.proprietario
    user = User.objects.get(id=id)
    paciente = Paciente.objects.get(user=user)
    if request.method == 'POST':
        card_form = FormCartao(request.POST)
        if card_form.is_valid():
            new_card = card_form.save(commit=False)
            new_card.paciente = paciente
            new_card.save()
            messages.success(request, 'Cartão cadastrado com Sucesso!')
            request.session['show_message'] = True 
            return redirect('adicionar_cartoes', id)
        else:
            messages.error(request, f"Formulário de cartão inválido: {card_form.errors}")
            request.session['show_message'] = True 
            return redirect('adicionar_cartoes', id)
    else:
        show_message = request.session.pop('show_message', False)
        bandeiras = BandeiraCartao.objects.all()
        return render(request, 'add_cartao (prop).html', {'proprietario': proprietario, 'bandeiras': bandeiras,'message_view': show_message})

@group_required('Proprietario')
@login_required    
def deleteCartao(request, id):
    proprietario = request.user.proprietario
    cartao = CadCartao.objects.get(id=id)
    paciente_card = cartao.paciente
    if request.method == 'POST':
        cartao.delete()
        return redirect('cartoes_prop', paciente_card.user.id)
    else:
        return render(request, 'delete_cartao (prop).html', {'proprietario': proprietario, 'cartao': cartao})

@group_required('Proprietario')
@login_required  
def mostrarConvenios(request):
    proprietario = request.user.proprietario
    convenios = Convenio.objects.all()

    return render(request, 'forn_convenio_list.html', {'proprietario': proprietario, 'convenios': convenios})

@group_required('Proprietario')
@login_required     
def addFornecedorConvenio(request):
    proprietario = request.user.proprietario
    if request.method == 'POST':
        fornecedor = EmpresaConvenio(request.POST)
        if fornecedor.is_valid():
            new_fornecedor = fornecedor.save(commit=False)
            new_fornecedor.save()
            messages.success(request, 'Fornecedor de convênio cadastrado com Sucesso!')
            request.session['show_message'] = True 
            return redirect('adicionar_convenio')
        else:
            messages.error(request, f"Cadastro de fornecerdor de convênio inválido: {fornecedor.errors}")
            request.session['show_message'] = True 
            return redirect('adicionar_convenio')
    else:
        show_message = request.session.pop('show_message', False)
        return render(request, 'add_convenio_empresa.html', {'proprietario': proprietario,'message_view': show_message})

@group_required('Proprietario')
@login_required    
def deleteConvenio(request, id):
    proprietario = request.user.proprietario
    convenio = Convenio.objects.get(id=id)
    if request.method == 'POST':
        convenio.delete()
        return redirect('convenios')
    else:
        return render(request, 'delete_convenio.html', {'proprietario': proprietario, 'convenio': convenio})

@group_required('Proprietario')
@login_required    
def mostrarPlano(request, id):
    proprietario = request.user.proprietario
    convenio = Convenio.objects.get(id=id)
    try:
        planos = PlanoConvenio.objects.filter(convenio=convenio)
    except:
        planos = ''
    finally:
        return render(request, 'planos_list.html', {'proprietario': proprietario, 'planos': planos, 'convenio': convenio})

@group_required('Proprietario')
@login_required 
def addPlano(request, id):
    proprietario = request.user.proprietario
    convenio = Convenio.objects.get(id=id)
    if request.method == 'POST':
        plano_form = CadPlano(request.POST)
        if plano_form.is_valid():
            new_plano = plano_form.save(commit=False)
            new_plano.convenio = convenio
            new_plano.save()
            messages.success(request, 'Plano cadastrado com Sucesso!')
            request.session['show_message'] = True 
            return redirect('adicionar_plano', id)
        else:
            messages.error(request, f"Formulário de plano inválido: {plano_form.errors}")
            request.session['show_message'] = True 
            return redirect('adicionar_plano', id)
    else:
        show_message = request.session.pop('show_message', False)
        return render(request, 'add_plano.html', {'proprietario': proprietario, 'convenio': convenio,'message_view': show_message})

@group_required('Proprietario')
@login_required 
def deletePlano(request, id):
    proprietario = request.user.proprietario
    plano = PlanoConvenio.objects.get(id=id)
    convenio = plano.convenio
    if request.method == 'POST':
        plano.delete()
        return redirect('planos_convenio', convenio.id)
    else:
        return render(request, 'delete_plano.html', {'proprietario': proprietario, 'plano': plano})

@group_required('Proprietario')
@login_required     
def cadConvPaciente(request,id):
    proprietario = request.user.proprietario
    user = User.objects.get(id=id)
    paciente = Paciente.objects.get(user=user)
    if request.method == 'POST':
        conv_form = FormConvenio(request.POST)
        if conv_form.is_valid():
            new_conv = conv_form.save(commit=False)
            new_conv.paciente = paciente
            new_conv.save()
            messages.success(request, 'Convênio do paciente cadastrado com Sucesso!')
            request.session['show_message'] = True 
            return redirect('adicionar_convenio_paciente', id)
        else:
            messages.error(request, f"Formulário de cartão inválido: {conv_form.errors}")
            request.session['show_message'] = True 
            return redirect('adicionar_convenio_paciente', id)
    else:
        convenios = Convenio.objects.all()
        planos = PlanoConvenio.objects.all()
        show_message = request.session.pop('show_message', False)
        return render(request, 'add_paciente_convenio (prop).html', {'proprietario': proprietario, 'convenios': convenios, 'planos':planos,'message_view': show_message})

@group_required('Proprietario')
@login_required     
def delPacienteConv(request, id):
    proprietario = request.user.proprietario
    convenio = CadConvenio.objects.get(id=id)
    paciente_conv = convenio.paciente
    if request.method == 'POST':
        convenio.delete()
        return redirect('convenios_paciente_prop', paciente_conv.user.id)
    else:
        return render(request, 'delete_paciente_convenio (prop).html', {'proprietario': proprietario, 'convenio': convenio})

@group_required('Proprietario')
@login_required     
def mostrarPacienteConvenio(request, id):
    proprietario = request.user.proprietario
    user = User.objects.get(id=id)
    paciente = Paciente.objects.get(user=user)
    try:
        convenios = CadConvenio.objects.filter(paciente=paciente)
    except:
        convenios = ''
    finally:
        return render(request, 'convenios_list (prop).html', {'proprietario': proprietario, 'paciente': paciente, 'convenios': convenios})

@group_required('Proprietario')
@login_required    
def mostrarFichas(request):
    proprietario = request.user.proprietario
    consultas = Consulta.objects.filter(data=date.today())

    return render(request, 'fichas (prop).html', {'proprietario': proprietario, 'consultas': consultas})

@group_required('Proprietario')
@login_required 
def abrirFicha(request, id):
    proprietario = request.user.proprietario
    consulta = Consulta.objects.get(id=id)
    if request.method == 'POST':
        consulta.status_consulta = 'Ficha Aberta'
        consulta.save()
        return redirect('fichas_prop')
    else:
        return render(request, 'abrir_ficha (prop).html', {'proprietario': proprietario, 'consulta': consulta})

@group_required('Proprietario')
@login_required    
def document_list(request, id):
    proprietario = request.user.proprietario
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

                return render(request, 'prontuario (prop).html', {'proprietario': proprietario,'paciente':paciente,'prontuario': prontuario, 'list_documents': list_documents.items(), 'documentos' : documentos, 'encaminhamentos': encaminhamentos, 'bioimpedancia': bioimpedancia, 'anexos': anexos})
            else:
                list_documents = ''
                return render(request, 'prontuario (prop).html', {'proprietario': proprietario, 'paciente':paciente,'prontuario': prontuario, 'list_documents': list_documents})
    except:
        prontuario = ''
        return render(request, 'prontuario (prop).html', {'proprietario': proprietario, 'paciente':paciente, 'prontuario': prontuario, 'listdocumentos': ''})

@group_required('Proprietario')
@login_required         
def info_prontuario(request, id):
    proprietario = request.user.proprietario
    user = User.objects.get(id=id)
    paciente = Paciente.objects.get(user=user)
    prontuario = Prontuario.objects.get(paciente=paciente)
    return render(request, 'info_prontuario (prop).html', {'proprietario': proprietario, 'paciente': paciente, 'prontuario': prontuario})

# Sistema de pagamento
@group_required('Proprietario')
@login_required 
def pagarConsulta(request):
    proprietario = request.user.proprietario
    atendimento_data = request.session.get('atendimento_data')
    if not atendimento_data:
        messages.error(request, 'Dados da consulta não encontrados. Por favor, tente agendar novamente.')
        return redirect('agendamento')
    
    if request.method == 'POST':
        select = request.POST.get('forma_pag')
        if select == 'cartao':
            return redirect('pay_card_prop')
        elif select == 'convenio':
            return redirect('pay_conv_prop')
        elif select == 'boleto':
            return redirect('pay_bol_prop')
        elif select == 'pix':
            return redirect('pay_pix_prop')
    else:
        tratamentos = Tratamento.objects.filter(especialidade= Especialidade.objects.get(id=atendimento_data['especialidade_id']))
        total = 0
        for tratamento in tratamentos:
            total += tratamento.preco

        return render(request, 'pagamento (prop).html', {'proprietario': proprietario, 'consulta': atendimento_data, 'tratamentos':tratamentos, 'total':total})

@group_required('Proprietario')
@login_required 
def pagarConsultaCard(request):
    proprietario = request.user.proprietario
    atendimento_data = request.session.get('atendimento_data')
    anexo_files = request.session.get('anexo_files')
    cartoes = CadCartao.objects.filter(paciente = Paciente.objects.get(id=atendimento_data['paciente_id']))
    
    if not atendimento_data:
        messages.error(request, 'Dados da consulta não encontrados. Por favor, tente agendar novamente.')
        return redirect('agendamento')
    
    if request.method == 'POST':
        pay_form = PagamentoCard(request.POST)
        if pay_form.is_valid():
            pay = pay_form.save(commit=False)
            pay.paciente = Paciente.objects.get(id=atendimento_data['paciente_id'])
            pay.medico = Medico.objects.get(id=atendimento_data['medico_id']) 
            pay.forma_pagamento = 'Cartao'
            pay.status_pagamento = 'Aguardando pagamento'
            
            # Criar a consulta após a confirmação do pagamento
            new_atendimento = Consulta(
                paciente=Paciente.objects.get(id=atendimento_data['paciente_id']),
                tipo_consulta=atendimento_data['tipo_consulta'],
                medico= Medico.objects.get(id=atendimento_data['medico_id']),
                data=atendimento_data['data'],
                hora=atendimento_data['hora'],
                especialidade=Especialidade.objects.get(id=atendimento_data['especialidade_id']),
                status_consulta='Agendada'
            )
            pay.tratamento = Tratamento.objects.get(especialidade=new_atendimento.especialidade)
            pay.consulta = new_atendimento
            new_atendimento.save()
            pay.save()
            
            for arquivo_path in anexo_files:
                with open(arquivo_path, 'rb') as f:
                    django_file = File(f, name=os.path.basename(arquivo_path))
                    AnexoConsulta.objects.create(consulta=new_atendimento, arquivo=django_file)
                os.remove(arquivo_path)  # Deletar arquivo temporário
            
            request.session['show_message'] = True 
            messages.success(request, 'Consulta agendada com Sucesso!')
            return redirect('consultas')
        else:
            request.session['show_message'] = True 
            messages.error(request, 'Erro no pagamento.')
            return redirect('pay_card_prop')
    else:
        show_message = request.session.pop('show_message', False)
        return render(request, 'pay_card (prop).html', {'proprietario': proprietario, 'consulta': atendimento_data, 'cartoes': cartoes, 'message_view': show_message})

@group_required('Proprietario')  
@login_required 
def pagarConsultaConv(request):
    proprietario = request.user.proprietario
    atendimento_data = request.session.get('atendimento_data')
    anexo_files = request.session.get('anexo_files')
    convenios = CadConvenio.objects.filter(paciente = Paciente.objects.get(id=atendimento_data['paciente_id']))
    
    if not atendimento_data:
        messages.error(request, 'Dados da consulta não encontrados. Por favor, tente agendar novamente.')
        return redirect('agendamento')
    
    if request.method == 'POST':
        pay_form = PagamentoConv(request.POST)
        if pay_form.is_valid():
            pay = pay_form.save(commit=False)
            pay.paciente = Paciente.objects.get(id=atendimento_data['paciente_id'])
            pay.medico = Medico.objects.get(id=atendimento_data['medico_id']) 
            pay.forma_pagamento = 'Convenio'
            pay.status_pagamento = 'Aguardando pagamento'
            
            # Criar a consulta após a confirmação do pagamento
            new_atendimento = Consulta(
                paciente=Paciente.objects.get(id=atendimento_data['paciente_id']),
                tipo_consulta=atendimento_data['tipo_consulta'],
                medico= Medico.objects.get(id=atendimento_data['medico_id']),
                data=atendimento_data['data'],
                hora=atendimento_data['hora'],
                especialidade=Especialidade.objects.get(id=atendimento_data['especialidade_id']),
                status_consulta='Agendada'
            )
            pay.tratamento = Tratamento.objects.get(especialidade=new_atendimento.especialidade)
            pay.consulta = new_atendimento
            new_atendimento.save()
            pay.save()
            
            for arquivo_path in anexo_files:
                with open(arquivo_path, 'rb') as f:
                    django_file = File(f, name=os.path.basename(arquivo_path))
                    AnexoConsulta.objects.create(consulta=new_atendimento, arquivo=django_file)
                os.remove(arquivo_path)  # Deletar arquivo temporário
            
            request.session['show_message'] = True
            messages.success(request, 'Consulta agendada com Sucesso!')
            return redirect('consultas')
        else:
            request.session['show_message'] = True 
            messages.error(request, 'Erro no pagamento.')
            return redirect('pay_conv_prop')
    else:
        show_message = request.session.pop('show_message', False)
        return render(request, 'pay_conv (prop).html', {'proprietario': proprietario, 'consulta': atendimento_data, 'convenios': convenios, 'message_view': show_message})

@group_required('Proprietario')
@login_required 
def pagarConsultaBol(request):
    proprietario = request.user.proprietario
    atendimento_data = request.session.get('atendimento_data')
    anexo_files = request.session.get('anexo_files')
   
    if not atendimento_data:
        messages.error(request, 'Dados da consulta não encontrados. Por favor, tente agendar novamente.')
    
        # Criar a consulta após a confirmação do pagamento
    consulta_existente = Consulta.objects.filter(
        paciente=Paciente.objects.get(id=atendimento_data['paciente_id']),
        tipo_consulta=atendimento_data['tipo_consulta'],
        medico=Medico.objects.get(id=atendimento_data['medico_id']),
        data=atendimento_data['data'],
        hora=atendimento_data['hora'],
        especialidade=Especialidade.objects.get(id=atendimento_data['especialidade_id']),
        status_consulta='Agendada'
    ).first()
   
    if consulta_existente:
        pagamento_existente = Pagamento.objects.get(consulta=consulta_existente)
        return render(request, 'pay_bol (prop).html', {'proprietario': proprietario, 'consulta': consulta_existente, 'boleto': pagamento_existente.boleto}) 
    else:
        new_atendimento = Consulta.objects.create(
            paciente=Paciente.objects.get(id=atendimento_data['paciente_id']),
            tipo_consulta=atendimento_data['tipo_consulta'],
            medico=Medico.objects.get(id=atendimento_data['medico_id']),
            data=atendimento_data['data'],
            hora=atendimento_data['hora'],
            especialidade=Especialidade.objects.get(id=atendimento_data['especialidade_id']),
            status_consulta='Agendada'
        )
        new_atendimento.save()

        pay = Pagamento.objects.create(
            paciente=Paciente.objects.get(id=atendimento_data['paciente_id']),
            medico=Medico.objects.get(id=atendimento_data['medico_id']),
            forma_pagamento='Boleto',
            tratamento=Tratamento.objects.get(especialidade=new_atendimento.especialidade),
            consulta=new_atendimento,
            status_pagamento='Aguardando pagamento',
            data_emissao=date.today()
        )
        pay.save()

        bol = Boleto.objects.create(pagamento = pay)
        bol.save()

        for arquivo_path in anexo_files:
            with open(arquivo_path, 'rb') as f:
                django_file = File(f, name=os.path.basename(arquivo_path))
                AnexoConsulta.objects.create(consulta=new_atendimento, arquivo=django_file)
            os.remove(arquivo_path)  # Deletar arquivo temporário

        return render(request, 'pay_bol (prop).html', {'proprietario': proprietario, 'consulta': atendimento_data, 'boleto': bol})

@group_required('Proprietario')
@login_required    
def addTratamento(request):
    proprietario = request.user.proprietario
    especialidades = Especialidade.objects.all()
    if request.method == 'POST':
        tra_form = CadTratamento(request.POST)
        if tra_form.is_valid():
            new_tratamento = tra_form.save(commit=False)
            new_tratamento.save()
            messages.success(request, 'Tratamento Cadastrado com Sucesso!')
            request.session['show_message'] = True 
            return redirect('adicionar_tratamento')
        else:
            messages.error(request, f"Formulário de cadastro inválido: {tra_form.errors}")
            request.session['show_message'] = True 
            return redirect('adicionar_tratamento')
    else:
        show_message = request.session.pop('show_message', False)
        return render(request, 'add_tratamento.html', {'proprietario': proprietario, 'especialidades': especialidades,'message_view': show_message})

@group_required('Proprietario')
@login_required    
def mostrarTratamentos(request):
    proprietario = request.user.proprietario
    tratamentos = Tratamento.objects.all()
    return render(request, 'tratamentos_list.html', {'proprietario': proprietario, 'tratamentos': tratamentos})

@group_required('Proprietario')
@login_required 
def dadosTratamento(request, id):
    proprietario = request.user.proprietario
    tratamento = Tratamento.objects.get(id=id)
    especialidades = Especialidade.objects.all()
    if request.method == 'POST':
        edit_paciente_form = CadTratamento(request.POST, instance=tratamento)
        if edit_paciente_form.is_valid():
            edit_paciente_form.save(commit=False)
            tratamento.save()
            request.session['show_message'] = True 
            messages.success(request, 'Dados do tratamento editados com Sucesso!')
            return redirect('tratamento', id=id)
        else:
            request.session['show_message'] = True 
            messages.error(request, f"Edição inválida: {edit_paciente_form.errors}")
            return redirect('tratamento', id=id)
    else:
        show_message = request.session.pop('show_message', False)
        return render(request, 'tratamento_data.html', {'proprietario': proprietario, 'tratamento': tratamento, 'especialidades': especialidades,'message_view': show_message})

@group_required('Proprietario')
@login_required     
def deleteTratamento(request, id):
    proprietario = request.user.proprietario
    tratamento = Tratamento.objects.get(id=id)
    if request.method == 'POST':
        tratamento.delete()
        return redirect('tratamentos')
    else:
        return render(request, 'delete_tratamento.html', {'proprietario': proprietario, 'tratamento': tratamento})

@group_required('Proprietario')
@login_required    
def mostrarPix(request):
    proprietario = request.user.proprietario
    pix = Pix.objects.all()

    return render(request, 'pix_list.html', {'proprietario': proprietario, 'pix': pix})

@group_required('Proprietario')
@login_required     
def addChave(request):
    proprietario = request.user.proprietario
    if request.method == 'POST':
        pix_form = CadPix(request.POST)
        if pix_form.is_valid():
            new_key = pix_form.save(commit=False)
            new_key.save()
            return redirect('pix')
        else:
            messages.error(request, f"Formulário de chave pix inválido: {pix_form.errors}")
            request.session['show_message'] = True 
            return redirect('adicionar_chave')
    else:
        show_message = request.session.pop('show_message', False)
        return render(request, 'add_chave.html', {'proprietario': proprietario, 'message_view': show_message})

@group_required('Proprietario')
@login_required     
def deletePix(request, id):
    proprietario = request.user.proprietario
    pix = Pix.objects.get(id=id)
    if request.method == 'POST':
        pix.delete()
        return redirect('convenios')
    else:
        return render(request, 'delete_convenio.html', {'proprietario': proprietario, 'pix': pix})

@group_required('Proprietario')
@login_required     
def payPix(request):
    proprietario = request.user.proprietario
    atendimento_data = request.session.get('atendimento_data')
    anexo_files = request.session.get('anexo_files')
    pix = Pix.objects.all()

    if not atendimento_data:
        messages.error(request, 'Dados da consulta não encontrados. Por favor, tente agendar novamente.')
        return redirect('agendamento')
    
    if request.method == 'POST':
        pay_form = PagamentoPix(request.POST)
        if pay_form.is_valid():
            pay = pay_form.save(commit=False)
            pay.paciente = Paciente.objects.get(id=atendimento_data['paciente_id'])
            pay.medico = Medico.objects.get(id=atendimento_data['medico_id']) 
            pay.forma_pagamento = 'Pix'
            pay.status_pagamento = 'Aguardando pagamento'
            
            # Criar a consulta após a confirmação do pagamento
            new_atendimento = Consulta(
                paciente=Paciente.objects.get(id=atendimento_data['paciente_id']),
                tipo_consulta=atendimento_data['tipo_consulta'],
                medico= Medico.objects.get(id=atendimento_data['medico_id']),
                data=atendimento_data['data'],
                hora=atendimento_data['hora'],
                especialidade=Especialidade.objects.get(id=atendimento_data['especialidade_id']),
                status_consulta='Agendada'
            )
            pay.tratamento = Tratamento.objects.get(especialidade=new_atendimento.especialidade)
            pay.consulta = new_atendimento
            new_atendimento.save()
            pay.save()
            
            for arquivo_path in anexo_files:
                with open(arquivo_path, 'rb') as f:
                    django_file = File(f, name=os.path.basename(arquivo_path))
                    AnexoConsulta.objects.create(consulta=new_atendimento, arquivo=django_file)
                os.remove(arquivo_path)  # Deletar arquivo temporário

            return redirect('pix_prop', pay.pix.id)
        else:
            request.session['show_message'] = True 
            messages.error(request, 'Erro no pagamento.')
            return redirect('pay_pix_prop')
    else:
        show_message = request.session.pop('show_message', False)
        return render(request, 'pay_pix (prop).html', {'proprietario': proprietario, 'consulta': atendimento_data, 'pix': pix, 'message_view': show_message})

@group_required('Proprietario')
@login_required 
def chavePix (request, id):
    proprietario = request.user.proprietario
    pix = Pix.objects.get(id=id)

    return render(request, 'chave.html', {'proprietario': proprietario, 'pix': pix})

@group_required('Proprietario')
@login_required 
def mostrarContas(request, id):
    proprietario = request.user.proprietario
    user = User.objects.get(id=id)
    paciente = Paciente.objects.get(user=user)
    contas = Pagamento.objects.filter(paciente=paciente).select_related('boleto', 'cartao', 'convenio', 'pix')
    return render(request, 'financeiro (prop).html', {'proprietario': proprietario, 'paciente': paciente,'contas': contas})

@group_required('Proprietario')
@login_required 
def mostrarBoleto(request, id):
    proprietario = request.user.proprietario
    boleto = Boleto.objects.get(id=id)
    return render(request, 'pay_bol (prop).html', {'proprietario': proprietario, 'boleto': boleto})

@group_required('Proprietario')
@login_required 
def document(request, id):
    proprietario = request.user.proprietario
    documento = Documentos.objects.get(id=id)
    
    return render(request, 'documento (prop).html', {'proprietario': proprietario, 'documento': documento})

@group_required('Proprietario')
@login_required 
def encaminha(request, id):
    proprietario = request.user.proprietario
    encaminhamento = Encaminhamento.objects.get(id=id)
    
    return render(request, 'encaminhamento (prop).html', {'proprietario': proprietario, 'encaminhamento': encaminhamento})

@group_required('Proprietario')
@login_required 
def bio(request, id):
    proprietario = request.user.proprietario
    bioimpedancia = Bioimpedância.objects.get(id=id)
    
    return render(request, 'bioimpedancia (prop).html', {'proprietario': proprietario, 'bioimpedancia': bioimpedancia})  

@group_required('Proprietario')
@login_required 
def anexo(request, id):
    proprietario = request.user.proprietario
    anexo = AnexoConsulta.objects.get(id=id)
    
    return render(request, 'anexo (prop).html', {'proprietario': proprietario, 'documento': anexo})

@group_required('Proprietario')
@login_required 
def anexos_list(request, id):
    proprietario = request.user.proprietario
    consulta = Consulta.objects.get(id=id)
    anexos = AnexoConsulta.objects.filter(consulta=consulta)
    
    return render(request, 'anexos_list (prop).html', {'proprietario': proprietario, 'anexos': anexos})       
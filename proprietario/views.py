from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from clinica.models import BandeiraCartao, Convenio, PlanoConvenio, Tratamento, Pix
from clinica.forms import CadBandeira, EmpresaConvenio, CadPlano, CadTratamento, CadPix
from paciente.models import Paciente, Consulta, CadCartao, CadConvenio, AnexoConsulta, Documentos, Prontuario, Boleto, Pagamento
from paciente.forms import CadPaciente, AgendaConsulta, FormCartao, FormConvenio, AnexoForm, ProntuarioForm, PagamentoCard, PagamentoConv
from medico.models import Medico, Especialidade
from medico.forms import CadMedico, CadEspecialidade
from recept.models import Recepcionista
from recept.forms import CadRecep
from itertools import chain
from django.contrib.auth.models import User
from django.contrib import messages
from datetime import date
from collections import defaultdict

# Create your views here.
@login_required 
def proprietyBoard(request):
    proprietario = request.user.proprietario
    return render(request, 'proprietario.html', {'proprietario': proprietario})

def contaProprietario(request):
    proprietario = request.user.proprietario
    return render(request, 'myaccount_proprietario.html', {'proprietario': proprietario})

def mostrarPacientes(request):
    proprietario = request.user.proprietario
    pacientes = Paciente.objects.all()
    return render(request, 'pacientes_list (prop).html', {'proprietario': proprietario, 'pacientes': pacientes})

def mostrarFuncionarios(request):
    proprietario = request.user.proprietario
    medicos = Medico.objects.all()
    recepcionistas = Recepcionista.objects.all()

    funcionarios = list(chain(medicos, recepcionistas))

    return render(request, 'funcionarios_list (prop).html', {'proprietario': proprietario, 'funcionarios': funcionarios, 'medicos': medicos, 'recepcionistas': recepcionistas})

def mostrarEspecialidades(request):
    proprietario = request.user.proprietario
    especialidades = Especialidade.objects.all()
    return render(request, 'especialidades_list.html', {'proprietario': proprietario, 'especialidades': especialidades})

def dadosPaciente(request, id):
    proprietario = request.user.proprietario
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
        return render(request, 'paciente_data (prop).html', {'proprietario': proprietario, 'paciente': paciente})

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
            return render(request, 'medico_data (prop).html', {'proprietario': proprietario, 'medico': user.medico, 'especialidades': especialidades})
        elif hasattr(user, 'recepcionista'):
            return render(request, 'recepcionista_data (prop).html', {'proprietario': proprietario, 'recepcionista': user.recepcionista})
        
def dadosEspecialidade(request, id):
    proprietario = request.user.proprietario
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
        return render(request, 'especialidade.html', {'proprietario': proprietario, 'especialidade': especialidade})

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
        return render(request, 'add_recepcionista.html', {'proprietario': proprietario})
    
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
        return render(request, 'add_medico.html', {'proprietario': proprietario, 'especialidades': especialidades}) 
    
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

def deletePaciente(request, id):
    proprietario = request.user.proprietario
    paciente = User.objects.get(id=id)
    if request.method == 'POST':
        paciente.delete()
        return redirect('pacientes')
    else:
        return render(request, 'delete_paciente (prop).html', {'proprietario': proprietario, 'paciente': paciente.paciente})

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
        
def deleteEspecialidade(request, id):
    proprietario = request.user.proprietario
    especialidade = Especialidade.objects.get(id=id)
    if request.method == 'POST':
        especialidade.delete()
        return redirect('especialidades')
    else:
        return render(request, 'delete_especialidade.html', {'proprietario': proprietario, 'especialidade': especialidade})


def mostrarConsultas(request):
    proprietario = request.user.proprietario
    consultas = Consulta.objects.all()
    return render(request, 'consultas (prop).html', {'proprietario': proprietario, 'consultas': consultas})

def marcarConsulta(request):
    proprietario = request.user.proprietario
    especialidade = Especialidade.objects.all()
    if request.method == 'POST':
        atendimento_form = AgendaConsulta(request.POST, request.FILES)
        anexo_form = AnexoForm(request.POST, request.FILES)
        if atendimento_form.is_valid() and anexo_form.is_valid():
            atendimento_data = atendimento_form.cleaned_data
            anexo_files = [arquivo.name for arquivo in request.FILES.getlist('arquivos')]
            serializable_atendimento_data = {
                'paciente_id': atendimento_data['paciente'].id,
                'tipo_consulta': atendimento_data['tipo_consulta'],
                'medico_id': atendimento_data['medico'].id,
                'data': atendimento_data['data'].isoformat(),
                'hora': atendimento_data['hora'].isoformat(),
                'especialidade_id': atendimento_data['especialidade'].id,
            }

            request.session['atendimento_data'] = serializable_atendimento_data
            request.session['anexo_files'] = anexo_files

            return redirect('pay_prop')
        else:
            return redirect('agendamento')
    else:
        pacientes = Paciente.objects.all()
        medicos = Medico.objects.all()
        return render(request, 'agendamento (prop).html', {'proprietario': proprietario, 'medicos': medicos, 'pacientes': pacientes, 'especialidades': especialidade})
    
def cancelarConsulta(request, id):
    proprietario = request.user.proprietario
    consulta = Consulta.objects.get(id=id)
    if request.method == 'POST':
        consulta.status_consulta = 'Cancelada'
        consulta.save()
        return redirect('consultas')
    else:
        return render(request, 'cancelar_consulta (prop).html', {'proprietario': proprietario, 'consulta': consulta})
    
def mostrarBandeiras(request):
    proprietario = request.user.proprietario
    bandeiras = BandeiraCartao.objects.all()

    return render(request, 'bandeiras_cartao_list.html', {'proprietario': proprietario, 'bandeiras': bandeiras})

    
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
    
def deleteBandeira(request, id):
    proprietario = request.user.proprietario
    bandeira = BandeiraCartao.objects.get(id=id)
    if request.method == 'POST':
        bandeira.delete()
        return redirect('bandeiras')
    else:
        return render(request, 'delete_bandeira.html', {'proprietario': proprietario, 'bandeira': bandeira})
    
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
    
def deleteCartao(request, id):
    proprietario = request.user.proprietario
    cartao = CadCartao.objects.get(id=id)
    paciente_card = cartao.paciente
    if request.method == 'POST':
        cartao.delete()
        return redirect('cartoes_prop', paciente_card.user.id)
    else:
        return render(request, 'delete_cartao (prop).html', {'proprietario': proprietario, 'cartao': cartao})
    
def mostrarConvenios(request):
    proprietario = request.user.proprietario
    convenios = Convenio.objects.all()

    return render(request, 'forn_convenio_list.html', {'proprietario': proprietario, 'convenios': convenios})
    
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
    
def deleteConvenio(request, id):
    proprietario = request.user.proprietario
    convenio = Convenio.objects.get(id=id)
    if request.method == 'POST':
        convenio.delete()
        return redirect('convenios')
    else:
        return render(request, 'delete_convenio.html', {'proprietario': proprietario, 'convenio': convenio})
    
def mostrarPlano(request, id):
    proprietario = request.user.proprietario
    convenio = Convenio.objects.get(id=id)
    try:
        planos = PlanoConvenio.objects.filter(convenio=convenio)
    except:
        planos = ''
    finally:
        return render(request, 'planos_list.html', {'proprietario': proprietario, 'planos': planos, 'convenio': convenio})

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

def deletePlano(request, id):
    proprietario = request.user.proprietario
    plano = PlanoConvenio.objects.get(id=id)
    convenio = plano.convenio
    if request.method == 'POST':
        plano.delete()
        return redirect('planos_convenio', convenio.id)
    else:
        return render(request, 'delete_plano.html', {'proprietario': proprietario, 'plano': plano})
    
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
    
def delPacienteConv(request, id):
    proprietario = request.user.proprietario
    convenio = CadConvenio.objects.get(id=id)
    paciente_conv = convenio.paciente
    if request.method == 'POST':
        convenio.delete()
        return redirect('convenios_paciente_prop', paciente_conv.user.id)
    else:
        return render(request, 'delete_paciente_convenio (prop).html', {'proprietario': proprietario, 'convenio': convenio})
    
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
    
def mostrarFichas(request):
    proprietario = request.user.proprietario
    consultas = Consulta.objects.filter(data=date.today())

    return render(request, 'fichas (prop).html', {'proprietario': proprietario, 'consultas': consultas})

def abrirFicha(request, id):
    proprietario = request.user.proprietario
    consulta = Consulta.objects.get(id=id)
    if request.method == 'POST':
        consulta.status_consulta = 'Ficha Aberta'
        consulta.save()
        return redirect('fichas_prop')
    else:
        return render(request, 'abrir_ficha (prop).html', {'proprietario': proprietario, 'consulta': consulta})
    
def document_list(request, id):
    # Agrupar documentos por data
    proprietario = request.user.proprietario
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

                print(list_documents[document.data])
                return render(request, 'prontuario (prop).html', {'proprietario': proprietario,'paciente':paciente,'prontuario': prontuario, 'list_documents': list_documents.items()})
            else:
                list_documents = ''
                return render(request, 'prontuario (prop).html', {'proprietario': proprietario, 'paciente':paciente,'prontuario': prontuario, 'list_documents': list_documents})
    except:
        prontuario = ''
        return render(request, 'prontuario (prop).html', {'proprietario': proprietario, 'paciente':paciente, 'prontuario': prontuario, 'listdocumentos': ''})
    
def init_prontuario(request, id):
    proprietario = request.user.proprietario
    user = User.objects.get(id=id)
    paciente = Paciente.objects.get(user=user)
    if request.method == 'POST':
        prontuario_form = ProntuarioForm(request.POST)
        if prontuario_form.is_valid():
            new_prontuario = prontuario_form.save(commit=False)
            new_prontuario.paciente = paciente
            new_prontuario.save()
            messages.success(request, 'Convênio do paciente cadastrado com Sucesso!')
            return redirect('prontuario', id)
        else:
            messages.error(request, f"Formulário de cartão inválido: {prontuario_form.errors}")
            return redirect('prontuario', id)   
    else:
        return render(request, 'init_prontuario.html', {'proprietario': proprietario, 'paciente': paciente})
        
def info_prontuario(request, id):
    proprietario = request.user.proprietario
    user = User.objects.get(id=id)
    paciente = Paciente.objects.get(user=user)
    prontuario = Prontuario.objects.get(paciente=paciente)
    return render(request, 'info_prontuario (prop).html', {'proprietario': proprietario, 'paciente': paciente, 'prontuario': prontuario})

# Sistema de pagamento
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
    else:
        return render(request, 'pagamento (prop).html', {'proprietario': proprietario, 'consulta': atendimento_data})

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
            
            for arquivo_name in anexo_files:
                arquivo = request.FILES.get(arquivo_name)
                if arquivo:
                    AnexoConsulta.objects.create(consulta=new_atendimento, arquivo=arquivo)
            
            messages.success(request, 'Consulta agendada com Sucesso!')
            return redirect('consultas')
        else:
            messages.error(request, 'Erro no pagamento.')
            return redirect('pay_card_prop')
    else:
        return render(request, 'pay_card (prop).html', {'proprietario': proprietario, 'consulta': atendimento_data, 'cartoes': cartoes})
    

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
            
            for arquivo_name in anexo_files:
                arquivo = request.FILES.get(arquivo_name)
                if arquivo:
                    AnexoConsulta.objects.create(consulta=new_atendimento, arquivo=arquivo)
            
            messages.success(request, 'Consulta agendada com Sucesso!')
            return redirect('consultas')
        else:
            messages.error(request, 'Erro no pagamento.')
            return redirect('pay_conv_prop')
    else:
        return render(request, 'pay_conv (prop).html', {'proprietario': proprietario, 'consulta': atendimento_data, 'convenios': convenios})
    

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
        bol = Boleto.objects.create()
        bol.save()
        pay = Pagamento.objects.create(
            paciente=Paciente.objects.get(id=atendimento_data['paciente_id']),
            medico=Medico.objects.get(id=atendimento_data['medico_id']),
            boleto=bol,
            forma_pagamento='Convenio',
            tratamento=Tratamento.objects.get(especialidade=new_atendimento.especialidade),
            consulta=new_atendimento,
            status_pagamento='Aguardando pagamento',
            data_emissao=date.today()
        )
        pay.save()

        for arquivo_name in anexo_files:
            arquivo = request.FILES.get(arquivo_name)
            if arquivo:
                AnexoConsulta.objects.create(consulta=new_atendimento, arquivo=arquivo)

        messages.success(request, 'Consulta agendada com Sucesso!')
        return render(request, 'pay_bol (prop).html', {'proprietario': proprietario, 'consulta': atendimento_data, 'boleto': bol})
    
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
    
def mostrarTratamentos(request):
    proprietario = request.user.proprietario
    tratamentos = Tratamento.objects.all()
    return render(request, 'tratamentos_list.html', {'proprietario': proprietario, 'tratamentos': tratamentos})

def dadosTratamento(request, id):
    proprietario = request.user.proprietario
    tratamento = Tratamento.objects.get(id=id)
    especialidades = Especialidade.objects.all()
    if request.method == 'POST':
        edit_paciente_form = CadTratamento(request.POST, instance=tratamento)
        if edit_paciente_form.is_valid():
            edit_paciente_form.save(commit=False)
            tratamento.save()
            messages.success(request, 'Dados do tratamento editados com Sucesso!')
            return redirect('tratamento', id=id)
        else:
            messages.error(request, f"Edição inválida: {edit_paciente_form.errors}")
            return redirect('tratamento', id=id)
    else:
        show_message = request.session.pop('show_message', False)
        return render(request, 'tratamento_data.html', {'proprietario': proprietario, 'tratamento': tratamento, 'especialidades': especialidades,'message_view': show_message})
    
def deleteTratamento(request, id):
    proprietario = request.user.proprietario
    tratamento = Tratamento.objects.get(id=id)
    if request.method == 'POST':
        tratamento.delete()
        return redirect('tratamentos')
    else:
        return render(request, 'delete_tratamento.html', {'proprietario': proprietario, 'tratamento': tratamento})
    
def mostrarPix(request):
    proprietario = request.user.proprietario
    pix = Pix.objects.all()

    return render(request, 'pix_list.html', {'proprietario': proprietario, 'pix': pix})
    
def addChave(request):
    proprietario = request.user.proprietario
    if request.method == 'POST':
        pix_form = CadPix(request.POST)
        if pix_form.is_valid():
            new_key = pix_form.save(commit=False)
            new_key.save()
            messages.success(request, 'Chave Cadastrada com Sucesso!')
            request.session['show_message'] = True 
            return redirect('pix')
        else:
            messages.error(request, f"Formulário de chave pix inválido: {pix_form.errors}")
            request.session['show_message'] = True 
            return redirect('pix')
    else:
        show_message = request.session.pop('show_message', False)
        return render(request, 'add_chave.html', {'proprietario': proprietario, 'message_view': show_message})
    
def deletePix(request, id):
    proprietario = request.user.proprietario
    pix = Pix.objects.get(id=id)
    if request.method == 'POST':
        pix.delete()
        return redirect('convenios')
    else:
        return render(request, 'delete_convenio.html', {'proprietario': proprietario, 'pix': pix})
    
def payPix(request):
    pass

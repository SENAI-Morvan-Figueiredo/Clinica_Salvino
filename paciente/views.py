import logging
from django.shortcuts import render, redirect
from .forms import CadPaciente, FormCartao, FormConvenio, PagamentoCard, PagamentoConv, AgendaConsulta, AnexoForm, PagamentoPix
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Paciente, Consulta, CadCartao, CadConvenio, Pagamento, Boleto, AnexoConsulta, Bioimpedância, Documentos, Encaminhamento, Prontuario
from medico.models import Medico
from clinica.models import BandeiraCartao, Tratamento, Especialidade, Pix, PlanoConvenio, Convenio
from datetime import date
from collections import defaultdict
from itertools import chain
from clinica_salvino.decorators import group_required

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

@group_required('Paciente')
@login_required   
def pacienteBoard(request):
    paciente = request.user.paciente
    consultas = Consulta.objects.filter(paciente=paciente).order_by('data')[:5]
    return render(request, 'paciente.html', {'paciente': paciente, 'consultas': consultas})

@group_required('Paciente')
@login_required 
def contaPaciente(request):
    user = request.user
    paciente = Paciente.objects.get(user=user)
    if request.method == 'POST':
        edit_paciente_form = CadPaciente(request.POST, instance=paciente)
        if edit_paciente_form.is_valid():
            edit_paciente_form.save(commit=False)
            paciente.save()
            request.session['show_message'] = True 
            messages.success(request, 'Seus dados foram editados com Sucesso!')
            return redirect('conta_paciente')
        else:
            request.session['show_message'] = True 
            messages.error(request, f"Edição inválida: {edit_paciente_form.errors}")
            return redirect('conta_paciente')
    else:
        show_message = request.session.pop('show_message', False)
        return render(request, 'myaccount_paciente.html', {'paciente': paciente, 'message_view': show_message})

@group_required('Paciente')
@login_required 
def mostrarCartoes(request):
    paciente = request.user.paciente
    try:
        cartoes = CadCartao.objects.filter(paciente=paciente)
    except:
        cartoes = ''
    finally:
        return render(request, 'cartoes_list (paciente).html', {'paciente': paciente, 'cartoes': cartoes})

@group_required('Paciente')
@login_required    
def mostrarPacienteConvenio(request):
    paciente = request.user.paciente
    try:
        convenios = CadConvenio.objects.filter(paciente=paciente)
    except:
        convenios = ''
    finally:
        return render(request, 'convenios_list (paciente).html', {'paciente': paciente, 'convenios': convenios})

@group_required('Paciente')
@login_required 
def add_cartao(request):
    paciente = request.user.paciente
    if request.method == 'POST':
        card_form = FormCartao(request.POST)
        if card_form.is_valid():
            new_card = card_form.save(commit=False)
            new_card.paciente = paciente
            new_card.save()
            messages.success(request, 'Cartão cadastrado com Sucesso!')
            request.session['show_message'] = True 
            return redirect('add_cartao_paciente')
        else:
            messages.error(request, f"Formulário de cartão inválido: {card_form.errors}")
            request.session['show_message'] = True 
            return redirect('add_cartao_paciente')
    else:
        show_message = request.session.pop('show_message', False)
        bandeiras = BandeiraCartao.objects.all()
        return render(request, 'add_cartao (paciente).html', {'paciente': paciente, 'bandeiras': bandeiras,'message_view': show_message})

@group_required('Paciente')
@login_required 
def delete_cartao(request, id):
    paciente = request.user.paciente
    cartao = CadCartao.objects.get(id=id)
    if request.method == 'POST':
        cartao.delete()
        return redirect('cartoes_paciente')
    else:
        return render(request, 'delete_cartao (paciente).html', {'paciente': paciente, 'cartao': cartao})

@group_required('Paciente')
@login_required 
def add_convenio(request):
    paciente = request.user.paciente
    if request.method == 'POST':
        conv_form = FormConvenio(request.POST)
        if conv_form.is_valid():
            new_conv = conv_form.save(commit=False)
            new_conv.paciente = paciente
            new_conv.save()
            messages.success(request, 'Convênio do paciente cadastrado com Sucesso!')
            request.session['show_message'] = True 
            return redirect('add_convenio_paciente')
        else:
            messages.error(request, f"Formulário de cartão inválido: {conv_form.errors}")
            request.session['show_message'] = True 
            return redirect('add_convenio_paciente')
    else:
        convenios = Convenio.objects.all()
        planos = PlanoConvenio.objects.all()
        show_message = request.session.pop('show_message', False)
        return render(request, 'add_convenio (paciente).html', {'paciente': paciente, 'convenios': convenios, 'planos':planos,'message_view': show_message})

@group_required('Paciente')
@login_required 
def delete_convenio(request, id):
    paciente = request.user.paciente
    convenio = CadConvenio.objects.get(id=id)
    if request.method == 'POST':
        convenio.delete()
        return redirect('convenios_paciente')
    else:
        return render(request, 'delete_convenio (paciente).html', {'paciente': paciente, 'convenio': convenio})

@group_required('Paciente')
@login_required    
def agendamento_paciente(request):
    paciente = request.user.paciente
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
            tratamentos = Tratamento.objects.all()
            if tratamentos:
                return redirect('pagamento_paciente')
            else:
                messages.error(request, f"Não há tratamentos cadastrados pelo proprietário da clínica")
                request.session['show_message'] = True 
                return redirect('agendamento_paciente')
        else:
            messages.error(request, f"Agendamento inválido: {atendimento_form.errors}")
            request.session['show_message'] = True 
            return redirect('agendamento_paciente')
    else:
        show_message = request.session.pop('show_message', False)
        medicos = Medico.objects.all()
        return render(request, 'agendamento (paciente).html', {'paciente': paciente, 'medicos': medicos, 'especialidades': especialidade, 'message_view': show_message})

@group_required('Paciente')
@login_required 
def pagamento_paciente(request):
    paciente = request.user.paciente
    atendimento_data = request.session.get('atendimento_data')
    if not atendimento_data:
        messages.error(request, 'Dados da consulta não encontrados. Por favor, tente agendar novamente.')
        return redirect('agendamento')
    
    if request.method == 'POST':
        select = request.POST.get('forma_pag')
        if select == 'cartao':
            return redirect('pay_card_paciente')
        elif select == 'convenio':
            return redirect('pay_conv_paciente')
        elif select == 'boleto':
            return redirect('pay_bol_paciente')
        elif select == 'pix':
            return redirect('pay_pix_paciente')
    else:
        tratamentos = Tratamento.objects.filter(especialidade= Especialidade.objects.get(id=atendimento_data['especialidade_id']))
        total = 0
        for tratamento in tratamentos:
            total += tratamento.preco

        return render(request, 'pagamento.html', {'paciente': paciente, 'consulta': atendimento_data, 'tratamentos':tratamentos, 'total':total})

@group_required('Paciente')
@login_required 
def pagarConsultaCard(request):
    paciente = request.user.paciente
    atendimento_data = request.session.get('atendimento_data')
    anexo_files = request.session.get('anexo_files')
    cartoes = CadCartao.objects.filter(paciente = paciente)
    
    if not atendimento_data:
        messages.error(request, 'Dados da consulta não encontrados. Por favor, tente agendar novamente.')
        return redirect('agendamento')
    
    if request.method == 'POST':
        pay_form = PagamentoCard(request.POST)
        if pay_form.is_valid():
            pay = pay_form.save(commit=False)
            pay.paciente = paciente
            pay.medico = Medico.objects.get(id=atendimento_data['medico_id']) 
            pay.forma_pagamento = 'Cartao'
            pay.status_pagamento = 'Aguardando pagamento'
            
            # Criar a consulta após a confirmação do pagamento
            new_atendimento = Consulta(
                paciente=Paciente.objects.get(id=atendimento_data['especialidade_id']),
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
            
            return redirect('consultas_paciente')
        else:
            request.session['show_message'] = True 
            messages.error(request, 'Erro no pagamento.')
            return redirect('pay_card_paciente')
    else:
        show_message = request.session.pop('show_message', False)
        return render(request, 'pay_card (paciente).html', {'paciente': paciente, 'consulta': atendimento_data, 'cartoes': cartoes, 'message_view': show_message})

@group_required('Paciente')   
@login_required 
def pagarConsultaConv(request):
    paciente = request.user.paciente
    atendimento_data = request.session.get('atendimento_data')
    anexo_files = request.session.get('anexo_files')
    convenios = CadConvenio.objects.filter(paciente = paciente)
    
    if not atendimento_data:
        messages.error(request, 'Dados da consulta não encontrados. Por favor, tente agendar novamente.')
        return redirect('agendamento')
    
    if request.method == 'POST':
        pay_form = PagamentoConv(request.POST)
        if pay_form.is_valid():
            pay = pay_form.save(commit=False)
            pay.paciente = paciente
            pay.medico = Medico.objects.get(id=atendimento_data['medico_id']) 
            pay.forma_pagamento = 'Convenio'
            pay.status_pagamento = 'Aguardando pagamento'
            
            # Criar a consulta após a confirmação do pagamento
            new_atendimento = Consulta(
                paciente=Paciente.objects.get(id=atendimento_data['especialidade_id']),
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
            
            return redirect('consultas_paciente')
        else:
            request.session['show_message'] = True 
            messages.error(request, 'Erro no pagamento.')
            return redirect('pay_conv_prop')
    else:
        show_message = request.session.pop('show_message', False)
        return render(request, 'pay_conv (paciente).html', {'paciente': paciente, 'consulta': atendimento_data, 'convenios': convenios, 'message_view': show_message})

@group_required('Paciente')  
@login_required 
def pagarConsultaBol(request):
    paciente = request.user.paciente
    atendimento_data = request.session.get('atendimento_data')
    anexo_files = request.session.get('anexo_files')
   
    if not atendimento_data:
        messages.error(request, 'Dados da consulta não encontrados. Por favor, tente agendar novamente.')
    
        # Criar a consulta após a confirmação do pagamento
    consulta_existente = Consulta.objects.filter(
        paciente=Paciente.objects.get(id=atendimento_data['especialidade_id']),
        tipo_consulta=atendimento_data['tipo_consulta'],
        medico=Medico.objects.get(id=atendimento_data['medico_id']),
        data=atendimento_data['data'],
        hora=atendimento_data['hora'],
        especialidade=Especialidade.objects.get(id=atendimento_data['especialidade_id']),
        status_consulta='Agendada'
    ).first()
   
    if consulta_existente:
        pagamento_existente = Pagamento.objects.get(consulta=consulta_existente)
        return render(request, 'pay_bol (paciente).html', {'paciente': paciente, 'consulta': consulta_existente, 'boleto': pagamento_existente.boleto}) 
    else:
        new_atendimento = Consulta.objects.create(
            paciente=Paciente.objects.get(id=atendimento_data['especialidade_id']),
            tipo_consulta=atendimento_data['tipo_consulta'],
            medico=Medico.objects.get(id=atendimento_data['medico_id']),
            data=atendimento_data['data'],
            hora=atendimento_data['hora'],
            especialidade=Especialidade.objects.get(id=atendimento_data['especialidade_id']),
            status_consulta='Agendada'
        )
        new_atendimento.save()

        pay = Pagamento.objects.create(
            paciente=Paciente.objects.get(id=atendimento_data['especialidade_id']),
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

        for arquivo_name in anexo_files:
            arquivo = request.FILES.get(arquivo_name)
            if arquivo:
                AnexoConsulta.objects.create(consulta=new_atendimento, arquivo=arquivo)

        return render(request, 'pay_bol (paciente).html', {'paciente': paciente, 'consulta': atendimento_data, 'boleto': bol})

@group_required('Paciente')
@login_required     
def payPix(request):
    paciente = request.user.paciente
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
            
            for arquivo_name in anexo_files:
                arquivo = request.FILES.get(arquivo_name)
                if arquivo:
                    AnexoConsulta.objects.create(consulta=new_atendimento, arquivo=arquivo)
            
            return redirect('pix_paciente', pay.pix.id)
        else:
            request.session['show_message'] = True 
            messages.error(request, 'Erro no pagamento.')
            return redirect('pay_pix_paciente')
    else:
        show_message = request.session.pop('show_message', False)
        return render(request, 'pay_pix (paciente).html', {'paciente': paciente, 'consulta': atendimento_data, 'pix': pix, 'message_view': show_message})

@group_required('Paciente')
@login_required 
def mostrarConsultas(request):
    paciente = request.user.paciente
    consultas = Consulta.objects.filter(paciente=paciente).order_by('status_consulta')
    return render(request, 'consultas (paciente).html', {'paciente': paciente, 'consultas': consultas})

@group_required('Paciente')
@login_required 
def cancelarConsulta(request, id):
    paciente = request.user.paciente
    consulta = Consulta.objects.get(id=id)
    pagameto = Pagamento.objects.get(consulta=consulta)
    if request.method == 'POST':
        consulta.status_consulta = 'Cancelada'
        pagameto.status_pagamento = 'Cancelado'
        pagameto.save()
        consulta.save()
        return redirect('consultas_paciente')
    else:
        return render(request, 'cancelar_consulta (paciente).html', {'paciente': paciente, 'consulta': consulta})

@group_required('Paciente')
@login_required    
def chavePix (request, id):
    paciente = request.user.paciente
    pix = Pix.objects.get(id=id)

    return render(request, 'chave (paciente).html', {'paciente': paciente, 'pix': pix})

@group_required('Paciente')
@login_required 
def mostrarContas(request):
    paciente = request.user.paciente
    contas = Pagamento.objects.filter(paciente=paciente).select_related('boleto', 'cartao', 'convenio', 'pix')
    return render(request, 'financeiro (paciente).html', {'paciente': paciente,'contas': contas})

@group_required('Paciente')
@login_required 
def mostrarBoleto(request, id):
    paciente = request.user.paciente
    boleto = Boleto.objects.get(id=id)
    return render(request, 'pay_bol (paciente).html', {'paciente': paciente, 'boleto': boleto})

@group_required('Paciente')
@login_required 
def document_list(request):
    # Agrupar documentos por data
    paciente = request.user.paciente
    list_documents = defaultdict(list)
    try:
        prontuario = Prontuario.objects.get(paciente=paciente)
        if prontuario:
            documentos = Documentos.objects.filter(prontuario=prontuario).order_by('data')
            encaminhamentos = Encaminhamento.objects.filter(prontuario=prontuario).order_by('data')
            bioimpedancia = Bioimpedância.objects.filter(prontuario=prontuario).order_by('data')
            documents_list = list(chain(documentos, encaminhamentos, bioimpedancia))
            if documents_list:
                documents_list.sort(key=lambda x: x.data)
                for document in documents_list:
                    list_documents[document.data].append(document)

                return render(request, 'prontuario (paciente).html', {'paciente': paciente,'prontuario': prontuario, 'list_documents': list_documents.items(), 'documentos' : documentos, 'encaminhamentos': encaminhamentos, 'bioimpedancia': bioimpedancia})
            else:
                list_documents = ''
                return render(request, 'prontuario (paciente).html', {'paciente': paciente,'prontuario': prontuario, 'list_documents': list_documents})
    except:
        prontuario = ''
        return render(request, 'prontuario (paciente).html', {'paciente': paciente, 'prontuario': prontuario, 'listdocumentos': ''})

@group_required('Paciente')
@login_required   
def document(request, id):
    paciente = request.user.paciente
    documento = Documentos.objects.get(id=id)
    
    return render(request, 'documento (paciente).html', {'paciente':paciente, 'documento': documento})

@group_required('Paciente')
@login_required 
def encaminha(request, id):
    paciente = request.user.paciente
    encaminhamento = Encaminhamento.objects.get(id=id)
    
    return render(request, 'encaminhamento (paciente).html', {'paciente': paciente, 'encaminhamento': encaminhamento})

@group_required('Paciente')
@login_required 
def bio(request, id):
    paciente = request.user.paciente
    bioimpedancia = Bioimpedância.objects.get(id=id)
    
    return render(request, 'bioimpedancia (paciente).html', {'paciente': paciente, 'bioimpedancia': bioimpedancia})    
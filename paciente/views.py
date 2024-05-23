import logging
from django.shortcuts import render, redirect
from .forms import CadPaciente, FormCartao, FormConvenio, PagamentoCard, PagamentoConv, AgendaConsulta, AnexoForm, PagamentoPix
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Paciente, Consulta, CadCartao, CadConvenio, Pagamento, Boleto, AnexoConsulta
from medico.models import Medico
from clinica.models import BandeiraCartao, Tratamento, Especialidade, Pix, PlanoConvenio, Convenio
from datetime import date

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

@login_required   
def pacienteBoard(request):
    paciente = request.user.paciente
    consultas = Consulta.objects.filter(paciente=paciente)
    return render(request, 'paciente.html', {'paciente': paciente, 'consultas': consultas})

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
            return redirect('conta_proprietario')
        else:
            request.session['show_message'] = True 
            messages.error(request, f"Edição inválida: {edit_paciente_form.errors}")
            return redirect('conta_proprietario')
    else:
        show_message = request.session.pop('show_message', False)
        return render(request, 'myaccount_paciente.html', {'paciente': paciente, 'message_view': show_message})

def mostrarCartoes(request):
    paciente = request.user.paciente
    try:
        cartoes = CadCartao.objects.filter(paciente=paciente)
    except:
        cartoes = ''
    finally:
        return render(request, 'cartoes_list (paciente).html', {'paciente': paciente, 'cartoes': cartoes})

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
    
def mostrarPacienteConvenio(request):
    paciente = request.user.paciente
    try:
        convenios = CadConvenio.objects.filter(paciente=paciente)
    except:
        convenios = ''
    finally:
        return render(request, 'convenios_list (paciente).html', {'paciente': paciente, 'convenios': convenios})

def add_cartao(request):
    paciente = request.user.paciente
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
        return render(request, 'add_cartao (paciente).html', {'paciente': paciente, 'bandeiras': bandeiras,'message_view': show_message})

def delete_cartao(request, id):
    proprietario = request.user.proprietario
    cartao = CadCartao.objects.get(id=id)
    paciente_card = cartao.paciente
    if request.method == 'POST':
        cartao.delete()
        return redirect('cartoes_prop', paciente_card.user.id)
    else:
        return render(request, 'delete_cartao (prop).html', {'proprietario': proprietario, 'cartao': cartao})

def add_convenio(request):
    paciente = request.user.paciente
    return render(request, 'add_convenio(paciente).html', {'paciente': paciente}) 

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

            return redirect('pay_prop')
        else:
            return redirect('agendamento')
    else:
        pacientes = Paciente.objects.all()
        medicos = Medico.objects.all()
        return render(request, 'agendamento (prop).html', {'paciente': paciente, 'medicos': medicos, 'pacientes': pacientes, 'especialidades': especialidade})

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

        return render(request, 'pagamento (prop).html', {'paciente': paciente, 'consulta': atendimento_data, 'tratamentos':tratamentos, 'total':total})

def pagarConsultaCard(request):
    paciente = request.user.proprietario
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
            
            request.session['show_message'] = True 
            messages.success(request, 'Consulta agendada com Sucesso!')
            return redirect('consultas')
        else:
            request.session['show_message'] = True 
            messages.error(request, 'Erro no pagamento.')
            return redirect('pay_card_paciente')
    else:
        show_message = request.session.pop('show_message', False)
        return render(request, 'pay_card (prop).html', {'paciente': paciente, 'consulta': atendimento_data, 'cartoes': cartoes, 'message_view': show_message})
    

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
            
            request.session['show_message'] = True
            messages.success(request, 'Consulta agendada com Sucesso!')
            return redirect('consultas')
        else:
            request.session['show_message'] = True 
            messages.error(request, 'Erro no pagamento.')
            return redirect('pay_conv_prop')
    else:
        show_message = request.session.pop('show_message', False)
        return render(request, 'pay_conv (prop).html', {'paciente': paciente, 'consulta': atendimento_data, 'convenios': convenios, 'message_view': show_message})
    

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
        return render(request, 'pay_bol (prop).html', {'paciente': paciente, 'consulta': consulta_existente, 'boleto': pagamento_existente.boleto}) 
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

        return render(request, 'pay_bol (prop).html', {'paciente': paciente, 'consulta': atendimento_data, 'boleto': bol})
    
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
            
            request.session['show_message'] = True 
            messages.success(request, 'Consulta agendada com Sucesso!')
            return redirect('pix_prop', pay.pix.id)
        else:
            request.session['show_message'] = True 
            messages.error(request, 'Erro no pagamento.')
            return redirect('pay_pix_prop')
    else:
        show_message = request.session.pop('show_message', False)
        return render(request, 'pay_pix (prop).html', {'paciente': paciente, 'consulta': atendimento_data, 'pix': pix, 'message_view': show_message})

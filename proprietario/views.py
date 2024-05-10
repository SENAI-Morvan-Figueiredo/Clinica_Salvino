from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from clinica.models import BandeiraCartao, Convenio, PlanoConvenio
from clinica.forms import CadBandeira, EmpresaConvenio, CadPlano
from paciente.models import Paciente, Consulta, CadCartao, CadConvenio, AnexoConsulta, Documentos, Prontuario
from paciente.forms import CadPaciente, AgendaConsulta, FormCartao, FormConvenio, AnexoForm
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
            return redirect('adicionar_pacientes')
        else:
            messages.error(request, f"Formulário de cadastro inválido: {paciente_form.errors}")
            return redirect('adicionar_pacientes')
        
    else:
        return render(request, 'add_paciente (prop).html', {'proprietario': proprietario})

def addFuncionario(request):
    proprietario = request.user.proprietario
    if request.method == 'POST':
        tipo = request.POST['tipo_funcionario']
        if tipo == 'recepcionista':
            return redirect('adicionar_recep')
        elif tipo == 'medico':
            return redirect('adicionar_medico')
    else:
        return render(request, 'add_funcionario.html', {'proprietario': proprietario})

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
            return redirect('adicionar_funcionarios')
        else:
            messages.error(request, f"Formulário de cadastro inválido: {recepcionista_form.errors}")
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
            print(new_medico)
            new_medico.save()
            messages.success(request, 'Médico Cadastrado com Sucesso!')
            return redirect('adicionar_funcionarios')
        else:
            messages.error(request, f"Formulário de cadastro inválido: {medico_form.errors}")
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
            return redirect('adicionar_especialidade')
        else:
            messages.error(request, f"Formulário de cadastro inválido: {esp_form.errors}")
            return redirect('adicionar_especialidade')
    else:
        return render(request, 'add_especialidade.html', {'proprietario': proprietario})

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
            new_atendimento = atendimento_form.save(commit=False)
            new_atendimento.status_consulta = 'Agendada'
            new_atendimento.save()

            for arquivo in request.FILES.getlist('arquivos'):
                AnexoConsulta.objects.create(consulta=new_atendimento, arquivo=arquivo)

            messages.success(request, 'Consulta agendada com Sucesso!')
            return redirect('agendamento')
        else:
            messages.error(request, f"Formulário de agendamento inválido: {atendimento_form.errors}")
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
            return redirect('adicionar_bandeira')
        else:
            messages.error(request, f"Cadastro de bandeira inválido: {bandeira.errors}")
            return redirect('adicionar_bandeira')
    else:
        return render(request, 'add_bandeira_cartao.html', {'proprietario': proprietario})
    
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
            return redirect('adicionar_cartoes', id)
        else:
            messages.error(request, f"Formulário de cartão inválido: {card_form.errors}")
            return redirect('adicionar_cartoes', id)
    else:
        bandeiras = BandeiraCartao.objects.all()
        return render(request, 'add_cartao (prop).html', {'proprietario': proprietario, 'bandeiras': bandeiras})
    
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
            return redirect('adicionar_convenio')
        else:
            messages.error(request, f"Cadastro de fornecerdor de convênio inválido: {fornecedor.errors}")
            return redirect('adicionar_convenio')
    else:
        return render(request, 'add_convenio_empresa.html', {'proprietario': proprietario})
    
def deleteConvenio(request, id):
    proprietario = request.user.proprietario
    convenio = Convenio.objects.get(id=id)
    if request.method == 'POST':
        convenio.delete()
        return redirect('convenios')
    else:
        return render(request, 'delete_convenio.html', {'proprietario': proprietario, 'convenio': convenio})
    
def mostrarPlano(request, id):
    convenio = Convenio.objects.get(id=id)
    try:
        planos = PlanoConvenio.objects.filter(convenio=convenio)
    except:
        planos = ''
    finally:
        return render(request, 'planos_list.html', {'planos': planos, 'convenio': convenio})

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
            return redirect('adicionar_plano', id)
        else:
            messages.error(request, f"Formulário de plano inválido: {plano_form.errors}")
            return redirect('adicionar_plano', id)
    else:
        return render(request, 'add_plano.html', {'proprietario': proprietario, 'convenio': convenio})

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
            return redirect('adicionar_convenio_paciente', id)
        else:
            messages.error(request, f"Formulário de cartão inválido: {conv_form.errors}")
            return redirect('adicionar_convenio_paciente', id)
    else:
        convenios = Convenio.objects.all()
        planos = PlanoConvenio.objects.all()
        return render(request, 'add_paciente_convenio (prop).html', {'proprietario': proprietario, 'convenios': convenios, 'planos':planos})
    
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
    list_documents = defaultdict(list)
    user = User.objects.get(id=id)
    paciente = Paciente.objects.get(user=user)
    prontuario = Prontuario.objects.get(paciente=paciente)
    for document in Documentos.objects.filter(prontuario=prontuario).order_by('data'):
        list_documents[document.data].append(document)

    print(list_documents[document.data])
        
    return render(request, 'prontuario (prop).html', {'list_documents': list_documents.items()})

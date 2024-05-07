from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def receptBoard(request):
    recepcionista = request.user.recepcionista
    return render(request, 'recepcionista.html', {'recepcionista': recepcionista})

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
        return render(request, 'add_paciente.html', {'proprietario': proprietario})

def deletePaciente(request, id):
    proprietario = request.user.proprietario
    paciente = User.objects.get(id=id)
    if request.method == 'POST':
        paciente.delete()
        return redirect('pacientes')
    else:
        return render(request, 'delete_paciente.html', {'proprietario': proprietario, 'paciente': paciente.paciente})

def contaRecept(request):
    recepcionista = request.user.recepcionista
    return render(request, 'myaccount_recept.html', {'recepcionista': recepcionista})

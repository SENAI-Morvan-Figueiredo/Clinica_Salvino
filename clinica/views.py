from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth import authenticate, update_session_auth_hash, logout
from django.contrib.auth import login as Login_django
from paciente.models import Paciente, Consulta
from proprietario.models import Proprietario
from medico.models import Medico
from recept.models import Recepcionista
from proprietario.views import proprietyBoard
from medico.views import medBoard
from recept.views import receptBoard
from django.http import HttpResponseBadRequest
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.contrib.auth.decorators import login_required
from .forms import CustomPasswordChangeForm


def home(request):
    return render(request, 'index.html')

def nutris(request):
    return render(request, 'conhecaNossosNutris.html')

def contact_us(request):
    if request.POST:
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        assunto = request.POST.get('assunto')
        mensagem = request.POST.get('mensagem')
        try:
            send_mail(
                f'Mensagem de {nome}: {assunto}',
                f'Nome: {nome} \nEmail: {email} \nAssunto:{assunto} \n{mensagem}',
                "avelinogabrieldossantos@gmail.com",
                ["aluno103.23187221gabriel@gmail.com"],
                fail_silently=False,
            )
            messages.success(request, 'Formulário enviado com sucesso!')
            return redirect('contact')
        except:
            messages.error(request, 'Ocorreu um erro com a mensagem!')
            return redirect('contact')
    else:
        return render(request, 'contact-forms.html')
    
def login(request):
    if request.user.is_authenticated:
        # Se o usuário já estiver autenticado, redirecione-o para a área de dashboard correta
        if Paciente.objects.filter(user=request.user).exists():
            return redirect('paciente_dash')
        elif Proprietario.objects.filter(user=request.user).exists():
            return redirect('proprietario_dash')
        elif Medico.objects.filter(user=request.user).exists():
            return redirect('medico_dash')
        elif Recepcionista.objects.filter(user=request.user).exists():
            return redirect('recepcionista_dash')
        
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            try:
                if user:
                    Login_django(request, user)
                    if Paciente.objects.filter(user=user).exists():
                        return redirect('paciente_dash')
                    elif Proprietario.objects.filter(user=user).exists():
                        return redirect('proprietario_dash')
                    elif Medico.objects.filter(user=user).exists():
                        return redirect('medico_dash')
                    elif Recepcionista.objects.filter(user=user).exists():
                        return redirect('recepcionista_dash')
                else:
                    messages.error(request, "Credenciais inválidas. Por favor, verifique seu email e senha.")
                    return redirect('login')
            except:
                messages.error(request, "Tivemos um pequeno erro ao realizar seu login. Tente novamente.")
                return redirect('login')
    else:
        return render(request, 'login.html')

def logout_user(request):
    logout(request)
    return redirect('home')

def forgot(request):
    return render(request, 'forgot.html')

def change_email(request):
    return render(request, 'change-email.html')

@login_required
def change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.POST, user=request.user)
        if form.is_valid():
            user = request.user
            user.set_password(form.cleaned_data['new_password1'])
            user.save()
            update_session_auth_hash(request, user)  # Importante para manter o usuário logado após a troca de senha
            return redirect('login')
        else:
            messages.error(request, f"Formulário de cadastro inválido: {form.errors}")
            request.session['show_message'] = True 
            return redirect('login')
    else:
        show_message = request.session.pop('show_message', False)
        form = CustomPasswordChangeForm(user=request.user)
    
    return render(request, 'registration/change_password.html', {'form': form,'message_view': show_message})

@require_GET
def get_available_times(request):
    date = request.GET.get('date')
    especialidade = request.GET.get('especialidade')
    medico = request.GET.get('medico')
    
    if not date or not especialidade or not medico:
        return JsonResponse({'error': 'Dados incompletos'}, status=400)
    
    consultas = Consulta.objects.filter(data=date, especialidade=especialidade, medico=medico)
    booked_times = []

    for consulta in consultas:
        if consulta.status_consulta == 'Agendada':
            booked_times.append(consulta.hora.strftime('%H:%M:%S'))
    
    all_times = [
        "08:00:00", "08:30:00", "09:00:00", "09:30:00", "10:00:00", "10:30:00", "11:00:00", "11:30:00",
        "12:00:00", "13:00:00", "13:30:00", "14:00:00", "14:30:00", "15:00:00", "15:30:00", "16:00:00",
        "16:30:00", "17:00:00"
    ]
    
    available_times = [time for time in all_times if time not in booked_times]
    
    return JsonResponse({'available_times': available_times})

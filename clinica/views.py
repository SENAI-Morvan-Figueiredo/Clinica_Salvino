from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login as Login_django
from django.contrib.auth import logout
from paciente.models import Paciente
from proprietario.models import Proprietario
from medico.models import Medico
from recept.models import Recepcionista
from proprietario.views import proprietyBoard
from medico.views import medBoard
from recept.views import receptBoard
from django.http import HttpResponseBadRequest


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
                        return redirect('paciente')
                    elif Proprietario.objects.filter(user=user).exists():
                        return redirect('proprietario')
                    elif Medico.objects.filter(user=user).exists():
                        return redirect('medico')
                    elif Recepcionista.objects.filter(user=user).exists():
                        return redirect('recepcionista')
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

def change_password(request):
    return render(request, 'change-password.html')


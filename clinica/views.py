from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth import authenticate, update_session_auth_hash, logout
from django.contrib.auth import login as Login_django
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.contrib.auth.decorators import login_required
from paciente.models import Paciente, Consulta
from proprietario.models import Proprietario
from medico.models import Medico
from recept.models import Recepcionista
from .forms import CustomPasswordChangeForm, PasswordResetRequestForm


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

def password_reset_request(request):
    if request.method == "POST":
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            associated_users = User.objects.filter(username=email)
            if associated_users.exists():
                for user in associated_users:
                    subject = "Redefinição de senha solicitada"
                    email_template_name = "registration/password_reset_email.html"
                    c = {
                        "email": email,
                        'domain': get_current_site(request).domain,
                        'site_name': 'Clínica Salvino',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    email_content = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email_content, 'avelinogabrieldossantos@gmail.com', [user.email], fail_silently=False)
                    except Exception as e:
                        messages.error(request, f"Ocorreu um erro ao enviar o e-mail: {str(e)}")
                        return redirect('/email/falhou/')
                    return redirect('password_reset_done')
            else:
                messages.error(request, "Usuário com este e-mail não encontrado.")
                return redirect('password_reset')
    else:
        form = PasswordResetRequestForm()
        return render(request, "registration/reset_senha_form.html", {"form": form})
    
def reset_password(request, uidb64=None, token=None):
    if uidb64 is not None and token is not None:
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = get_object_or_404(User, pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        
        if user is not None and default_token_generator.check_token(user, token):
            if request.method == 'POST':
                form = CustomPasswordChangeForm(request.POST, user=user)
                if form.is_valid():
                    user.set_password(form.cleaned_data['new_password1'])
                    user.save()
                    update_session_auth_hash(request, user)  # Importante para manter o usuário logado após a troca de senha
                    return redirect('password_reset_complete')
                else:
                    messages.error(request, f"Troca de senha inválida: {form.errors}")
                    request.session['show_message'] = True 
                    return redirect('password_reset_confirm')
            else:
                show_message = request.session.pop('show_message', False)
                form = CustomPasswordChangeForm(user=user)
            
            return render(request, 'registration/change_password.html', {'form': form, 'message_view': show_message})
        else:
            messages.error(request, 'O link de redefinição de senha não é válido.')
            return redirect('password_reset_done')

    else:
        messages.error(request, 'O link de redefinição de senha está faltando informações.')
        return redirect('password_reset_done')

def change_email(request):
    return render(request, 'change-email.html')

def confirm_envio(request):
    return render(request, 'reset_senha_concluido.html')

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

from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages

def home(request):
    return render(request, 'index.html')

def nutris(request):
    return render(request, 'conhecaNossosNutris.html')

def contact_us(request):
    requisicao = ''
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

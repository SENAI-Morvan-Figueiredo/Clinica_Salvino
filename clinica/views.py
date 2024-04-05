from django.shortcuts import render, redirect
from django.core.mail import send_mail

def home(request):
    return render(request, 'index.html')

def contact_us(request):
    if request.POST:
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        assunto = request.POST.get('assunto')
        mensagem = request.POST.get('mensagem')
        send_mail(
            f'Mensagem de {nome}: {assunto}',
            f'Nome: {nome} \nEmail:{email} \nAssunto:{assunto} \n{mensagem}',
            "avelinogabrieldossantos@gmail.com",
            ["aluno103.23187221gabriel@gmail.com"],
            fail_silently=False,
        )
        return redirect(home)
    else:
        return render(request, 'contact-forms.html')

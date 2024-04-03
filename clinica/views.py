from django.shortcuts import render

def home(request):
    return render(request, 'index.html')

def contact_us(request):
    return render(request, 'contact-forms.html')

from django.shortcuts import render, redirect

def home(request):
    return render(request, 'index.html')

def contact_us(request):
    if request.POST:
        return redirect(home)
    else:
        return render(request, 'contact-forms.html')

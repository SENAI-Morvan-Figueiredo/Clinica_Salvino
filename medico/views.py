from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required 
def medBoard(request):
    medico = request.user.medico
    return render(request, 'nutricionista.html', {'medico': medico})
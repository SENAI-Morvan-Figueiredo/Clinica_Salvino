from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def receptBoard(request):
    recepcionista = request.user.recepcionista
    return render(request, 'recepcionista.html', {'recepcionista': recepcionista})

def contaRecept(request):
    recepcionista = request.user.recepcionista
    return render(request, 'myaccount_recept.html', {'recepcionista': recepcionista})

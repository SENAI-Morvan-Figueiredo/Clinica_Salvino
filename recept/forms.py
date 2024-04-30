from django import forms
from .models import Recepcionista

class CadRecep(forms.ModelForm):

    data_nascimento = forms.DateField()
    
    class Meta:
        model = Recepcionista
        fields = ('name', 'sexo', 'genero', 'rg', 'cpf', 'data_nascimento', 'telefone', 'cep', 'endereco', 'numero', 'complemento')
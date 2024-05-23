from django import forms
from .models import Recepcionista

class CadRecep(forms.ModelForm):

    data_nascimento = forms.DateField()
    
    class Meta:
        model = Recepcionista
        fields = ('name', 'sexo', 'genero', 'outro', 'rg', 'cpf', 'data_nascimento', 'telefone', 'cep', 'estado', 'cidade', 'bairro', 'logradouro', 'numero', 'complemento')
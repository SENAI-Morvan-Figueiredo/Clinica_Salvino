from django import forms
from .models import Recepcionista

class CadRecep(forms.ModelForm):

    class Meta:
        model = Recepcionista
        fields = ('name', 'sexo', 'genero', 'rg', 'cpf', 'data_nascimento', 'telefone', 'cep', 'endereco', 'numero', 'complemento')
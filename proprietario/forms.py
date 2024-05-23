from django import forms
from .models import Proprietario

class CadProprietario(forms.ModelForm):

    data_nascimento = forms.DateField()

    class Meta:
        model = Proprietario
        fields = ('name','data_nascimento', 'sexo', 'genero', 'outro', 'data_nascimento', 'rg', 'cpf', 'telefone', 'cep', 'estado', 'cidade', 'bairro', 'logradouro', 'numero', 'complemento')

from django import forms
from .models import Medico

class CadMedico(forms.ModelForm):

    data_nascimento = forms.DateField()

    class Meta:
        model = Medico
        fields = ('name', 'sexo', 'genero', 'rg', 'cpf', 'data_nascimento', 'crm', 'especialidade', 'telefone', 'cep', 'endereco', 'numero', 'complemento')
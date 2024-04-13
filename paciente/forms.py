from django import forms
from .models import Paciente

class CadPaciente(forms.ModelForm):

    data_nascimento = forms.DateField()

    class Meta:
        model = Paciente
        fields = ('data_nascimento', 'rg', 'cpf', 'status_dependencia', 'nome_responsavel', 'rg_responsavel', 'cpf_responsavel', 'telefone', 'cep', 'endereco', 'numero', 'complemento')
        
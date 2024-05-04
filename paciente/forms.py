from django import forms
from .models import Paciente, Consulta

class CadPaciente(forms.ModelForm):

    data_nascimento = forms.DateField()

    class Meta:
        model = Paciente
        fields = ('name','data_nascimento', 'sexo', 'genero', 'data_nascimento', 'rg', 'cpf', 'status_dependencia', 'nome_responsavel', 'rg_responsavel', 'cpf_responsavel', 'telefone', 'cep', 'endereco', 'numero', 'complemento')


class AgendaConsulta(forms.ModelForm):

    class Meta:
        model = Consulta
        fields = ('paciente', 'tipo_consulta', 'medico', 'data', 'hora', 'especialidade', 'file_documento')
        
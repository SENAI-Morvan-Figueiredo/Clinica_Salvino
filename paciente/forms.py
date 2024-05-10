from django import forms
from .models import Paciente, Consulta, CadCartao, CadConvenio, AnexoConsulta

class CadPaciente(forms.ModelForm):

    data_nascimento = forms.DateField()

    class Meta:
        model = Paciente
        fields = ('name','data_nascimento', 'sexo', 'genero', 'data_nascimento', 'rg', 'cpf', 'status_dependencia', 'nome_responsavel', 'rg_responsavel', 'cpf_responsavel', 'telefone', 'cep', 'endereco', 'numero', 'complemento')


class AgendaConsulta(forms.ModelForm):

    class Meta:
        model = Consulta
        fields = ('paciente', 'tipo_consulta', 'medico', 'data', 'hora', 'especialidade')

class FormCartao(forms.ModelForm):
        
    class Meta:
        model = CadCartao
        fields = ('bandeira_cartao', 'numero_cartao', 'cvc', 'data_vencimento')

class FormConvenio(forms.ModelForm):

    class Meta:
        model = CadConvenio
        fields = ('convenio', 'plano_convenio', 'numero_carteirinha')

class AnexoForm(forms.Form):
    class Meta:
        model = AnexoConsulta
        fields = ('consulta',)
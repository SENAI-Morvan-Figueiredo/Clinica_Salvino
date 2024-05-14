from django import forms
from .models import Paciente, Consulta, CadCartao, CadConvenio, AnexoConsulta, Prontuario, Pagamento

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

class AnexoForm(forms.ModelForm):
    class Meta:
        model = AnexoConsulta
        fields = ('consulta',)

class ProntuarioForm(forms.ModelForm):
    class Meta:
        model = Prontuario
        fields = ('peso', 'altura', 'alergia', 'doenca', 'fuma', 'bebe', 'uso_drogas', 'observacoes')

class PagamentoForm(forms.ModelForm):
    class Meta:
        model = Pagamento
        fields = ('forma_pagamento', 'convenio', 'cartao', 'pix', 'boleto', 'cod_barras', 'status_pagamento', 'data_pagamento')
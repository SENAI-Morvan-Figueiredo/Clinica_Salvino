from django import forms
from .models import Paciente, Consulta, CadCartao, CadConvenio, AnexoConsulta, Prontuario, Pagamento, Documentos, Encaminhamento, Bioimpedância

class CadPaciente(forms.ModelForm):

    data_nascimento = forms.DateField()

    class Meta:
        model = Paciente
        fields = ('name','data_nascimento', 'sexo', 'genero', 'outro', 'data_nascimento', 'rg', 'cpf', 'status_dependencia', 'nome_responsavel', 'rg_responsavel', 'cpf_responsavel', 'telefone', 'cep', 'estado', 'cidade', 'bairro', 'logradouro', 'numero', 'complemento')


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

class ProntuarioForm(forms.ModelForm):
    class Meta:
        model = Prontuario
        fields = ('peso', 'altura', 'alergia', 'doenca', 'fuma', 'bebe', 'uso_drogas', 'observacoes')

class PagamentoCard(forms.ModelForm):

    class Meta:
        model = Pagamento
        fields = ('cartao',)

class PagamentoConv(forms.ModelForm):

    class Meta:
        model = Pagamento
        fields = ('convenio',)

class PagamentoPix(forms.ModelForm):

    class Meta:
        model = Pagamento
        fields = ('pix',)

class addDocumento(forms.ModelForm):
    class Meta:
        model = Documentos
        fields = ('data', 'tipo_documento', 'nome_documento', 'file_documento', 'descricao')

class addEncaminhamento(forms.ModelForm):
    class Meta:
        model = Encaminhamento
        fields = ('data', 'tipo_encaminhamento', 'area', 'file_documento', 'descricao')

class addBioimpedância(forms.ModelForm):
    class Meta:
        model = Bioimpedância
        fields = ('data', 'peso', 'altura', 'massa_magra', 'massa_muscular', 'agua_corporal', 'densidade_ossea', 'gordura_visceral', 'gordura_corporal', 'taxa_metabolica', 'imc')
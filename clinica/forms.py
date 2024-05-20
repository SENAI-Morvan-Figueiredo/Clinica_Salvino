from django import forms
from .models import BandeiraCartao, Convenio, PlanoConvenio, Tratamento, Pix


class CadBandeira(forms.ModelForm):
        
    class Meta:
        model = BandeiraCartao
        fields = ('name',)

class EmpresaConvenio(forms.ModelForm):

    class Meta:
        model = Convenio
        fields =('name',)

class CadPlano(forms.ModelForm):

    class Meta:
        model = PlanoConvenio
        fields = ('name',)

class CadTratamento(forms.ModelForm):

    class Meta:
        model = Tratamento
        fields = ('name', 'especialidade', 'preco', 'descricao',)

class CadPix(forms.ModelForm):

    class Meta:
        model = Pix
        fields = ('nome_proprietario_pix', 'chave')

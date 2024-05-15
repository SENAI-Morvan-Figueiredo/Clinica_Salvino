from django import forms
from .models import BandeiraCartao, Convenio, PlanoConvenio


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

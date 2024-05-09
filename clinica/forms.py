from django import forms
from .models import BandeiraCartao


class CadBandeira(forms.ModelForm):
        
    class Meta:
        model = BandeiraCartao
        fields = ('name',)
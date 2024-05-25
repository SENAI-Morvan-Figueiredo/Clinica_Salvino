from django import forms
from .models import BandeiraCartao, Convenio, PlanoConvenio, Tratamento, Pix
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import get_user_model

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

class CustomPasswordChangeForm(forms.Form):
    new_password1 = forms.CharField(
        label='Nova Senha',
        widget=forms.PasswordInput(attrs={'class': 'input', 'placeholder': 'Nova Senha'})
    )
    new_password2 = forms.CharField(
        label='Confirmar Nova Senha',
        widget=forms.PasswordInput(attrs={'class': 'input', 'placeholder': 'Confirmar Nova Senha'})
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        new_password1 = cleaned_data.get('new_password1')
        new_password2 = cleaned_data.get('new_password2')

        if new_password1 and new_password2:
            if new_password1 != new_password2:
                raise forms.ValidationError('As novas senhas não coincidem')
        return cleaned_data

class PasswordResetRequestForm(forms.Form):
    email = forms.EmailField(max_length=254, widget=forms.EmailInput(attrs={'class': 'input', 'placeholder': 'Email'}), required=False)
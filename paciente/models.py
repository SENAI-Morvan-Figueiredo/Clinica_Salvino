from django.db import models
from django.core.exceptions import ValidationError
from .const import STATUS_DEPENDENCE_CHOICE
from django.contrib.auth.models import User
from clinica.models import Convenio, PlanoConvenio, BandeiraCartao, Tratamento, Pix
from medico.models import Medico, Especialidade
from django.contrib import admin
import datetime


# Create your models here.
class Paciente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=256, unique=True)
    sexo = models.CharField(max_length=25, choices=(('Masculino', 'Masculino'), ('Feminino', 'Feminino'), ('Outro', 'Outro')))
    genero = models.CharField(max_length=256)
    data_nascimento = models.DateField(auto_created=False, auto_now=False, auto_now_add=False)
    rg = models.CharField(max_length=9)
    cpf = models.CharField(max_length=11)
    status_dependencia = models.CharField(max_length=20, choices=STATUS_DEPENDENCE_CHOICE)
    nome_responsavel = models.CharField(max_length=256, blank=True, null=True)
    rg_responsavel = models.CharField(max_length=9, blank=True, null=True)
    cpf_responsavel = models.CharField(max_length=11, blank=True, null=True)
    telefone = models.CharField(max_length=14)
    cep = models.CharField(max_length=8)
    endereco = models.TextField()
    numero = models.CharField(max_length=10)
    complemento = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.user.username

    def clean(self):
        if self.status_dependencia == 'Dependente' and not self.nome_responsavel:
            raise ValidationError({'nome_responsavel': 'O nome do responsável é obrigatório para pacientes dependentes.'})
        
        if self.status_dependencia == 'Dependente' and not self.rg_responsavel:
            raise ValidationError({'nome_responsavel': 'O nome do responsável é obrigatório para pacientes dependentes.'})
        
        if self.status_dependencia == 'Dependente' and not self.cpf_responsavel:
            raise ValidationError({'nome_responsavel': 'O nome do responsável é obrigatório para pacientes dependentes.'})


class Consulta(models.Model):
    paciente = models.ForeignKey(Paciente,on_delete=models.CASCADE)
    tipo_consulta = models.CharField(max_length=256, choices=(('Presencial', 'Presencial'), ('Remoto', 'Remoto')))
    medico = models.ForeignKey(Medico,on_delete=models.CASCADE)
    data = models.DateField(auto_created=False, auto_now=False, auto_now_add=False)
    hora = models.TimeField(auto_created=False, auto_now=False, auto_now_add=False)
    especialidade = models.ForeignKey(Especialidade,on_delete=models.CASCADE)
    file_documento = models.FileField(upload_to='exames/', null=True, blank=True)
    status_consulta =models.CharField(max_length=256, choices=(('Concluida','Concluida'), ('Cancelada','Cancelada'), ('Agendada','Agendada'),('Ficha Aberta','Ficha Aberta')))

    def __str__(self):
        return f'{self.paciente.name}  - {self.data}/{self.hora}'


class Prontuario(models.Model):
    paciente = models.OneToOneField(Paciente, on_delete=models.CASCADE)
    nome = models.CharField(max_length=256)
    peso = models.DecimalField(max_digits= 5, decimal_places= 2 )
    altura = models.DecimalField(max_digits=3 , decimal_places= 2)
    alergia = models.BooleanField()
    doenca = models.BooleanField()
    fuma = models.BooleanField()
    bebe = models.BooleanField()
    uso_drogas = models.BooleanField()
    observacoes = models.TextField(null=True)

    def __str__(self):
        return self.paciente.name
    
class Documentos(models.Model):
    prontuario = models.ForeignKey(Prontuario, on_delete= models.CASCADE)
    nome_documento = models.CharField(max_length=256)
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE)
    tipo_documento = models.CharField(max_length=256, choices=(('Descrição de Atendimento', 'Descrição de Atendimento'), ('Receita', 'Receita'), ('Dieta', 'Dieta')))
    data = models.DateField(auto_created=False, auto_now=False, auto_now_add=False)
    descricao = models.TextField(null=True)
    file_documento = models.FileField(upload_to='exames/', null=True, blank=True)

    def __str__(self):
        return self.nome_documento
    
    class Meta:
        verbose_name_plural = 'Documentos'

class Encaminhamento(models.Model):
    prontuario = models.ForeignKey(Prontuario, on_delete= models.CASCADE)
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE)
    data = models.DateField(auto_created=False, auto_now=False, auto_now_add=False)
    tipo_encaminhamento = models.CharField(max_length=256, choices=(('Consultas', 'Consultas'), ('Exames e Terapias', 'Exames e Terapias'), ('Outros', 'Outros')))
    area = models.CharField(max_length=256)
    descricao = models.TextField(null=True)
    file_documento = models.FileField(upload_to='exames/')

    def __str__(self):
        return self.tipo_encaminhamento
    
    class Meta:
        verbose_name_plural = 'Documentos'

class Bioimpedância(models.Model):
    prontuario = models.ForeignKey(Prontuario, on_delete= models.CASCADE)
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE)
    data = models.DateField(auto_created=False, auto_now=False, auto_now_add=False)
    peso = models.DecimalField(max_digits= 5, decimal_places= 2)
    altura = models.DecimalField(max_digits=3 , decimal_places= 2)
    massa_magra = models.DecimalField(max_digits= 5, decimal_places= 2 )
    massa_muscular = models.DecimalField(max_digits= 5, decimal_places= 2)
    agua_corporal = models.DecimalField(max_digits= 5, decimal_places= 2)
    densidade_ossea = models.DecimalField(max_digits= 5, decimal_places= 2 )
    gordura_visceral = models.DecimalField(max_digits= 5, decimal_places= 2 )
    gordura_corporal = models.DecimalField(max_digits= 5, decimal_places= 2 )
    taxa_metabolica = models.DecimalField(max_digits= 5, decimal_places= 2 )
    imc = models.DecimalField(max_digits= 4, decimal_places= 2 )

    def __str__(self):
        return self.data
    
    class Meta:
        verbose_name_plural = 'Documentos'


class CadConvenio(models.Model):
    paciente = models.OneToOneField(Paciente, on_delete=models.CASCADE)
    convenio = models.ForeignKey(Convenio, on_delete=models.CASCADE)
    plano_convenio = models.ForeignKey(PlanoConvenio, on_delete=models.CASCADE)
    numero_carteirinha = models.CharField(max_length=256)

    def __str__(self):
        return f'{self.convenio.name}: {self.plano_convenio.name}'
    
    class Meta:
        verbose_name_plural = 'CadConvenio'

        constraints = [
            models.UniqueConstraint(fields=['convenio', 'plano_convenio'], name='unique_convenio_plano_convenio')
        ]


class CadCartao(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    bandeira_cartao = models.ForeignKey(BandeiraCartao, on_delete=models.CASCADE)
    numero_cartao = models.CharField(max_length=256)
    cvc = models.CharField(max_length=3)
    data_vencimento = models.CharField(max_length=7)
    

    def clean(self):
        # Remove todos os caracteres que não são dígitos
        cleaned_value = ''.join(filter(str.isdigit, self.data_vencimento))
        
        # Adiciona a barra após os primeiros dois dígitos
        if len(cleaned_value) > 2:
            cleaned_value = cleaned_value[:2] + '/' + cleaned_value[2:]

        self.data_vencimento = cleaned_value

    def __str__(self):
        return self.data_vencimento
    

    class Meta:
        verbose_name_plural = 'CadCartao'


class Pagamento(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    data_emissao = models.DateField(auto_created=False, auto_now=False, auto_now_add=False)
    tratamento = models.ForeignKey(Tratamento, on_delete=models.CASCADE)
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE)
    forma_pagamento = models.CharField(max_length=256, choices=(('Convenio', 'Convenio'), ('Cartao', 'Cartao'), ('Pix', 'Pix'), ('Boleto', 'Boleto'), ('Pagar no dia', 'Pagar no dia')))
    convenio = models.ForeignKey(CadConvenio, blank=True, null=True, on_delete=models.SET_NULL)
    cartao = models.ForeignKey(CadCartao, blank=True, null=True, on_delete=models.SET_NULL)
    pix = models.ForeignKey(Pix, blank=True, null=True, on_delete=models.SET_NULL)
    boleto = models.FileField(upload_to='boletos/', blank=True, null=True)
    cod_barras =models.CharField(max_length=44, blank=True,null=True)
    status_pagamento = models.CharField(max_length=256, choices=(('Pago', 'Pago'), ('Aguardando pagamento', 'Aguardando pagamento'), ('Cancelado', 'Cancelado'), ('Aguardando reembolso', 'Aguardando reembolso'), ('Reembolsado', 'Reembolsado')))
    data_pagamento = models.CharField(max_length=256,blank=True, null=True)

    def clean(self):
        if self.forma_pagamento == 'Cartao' and not self.cartao:
            raise ValidationError({'cartao':'Você não selecionou um cartão cadastrado'})
        
        if self.forma_pagamento == 'Convenio' and not self.convenio:
            raise ValidationError({'convenio':'Você não selecionou um convênio cadastrado'})
        
        if self.forma_pagamento == 'Pix' and not self.pix:
            raise ValidationError({'pix':'Você não selecionou um pix cadastrado'})
        
        if self.forma_pagamento == 'Boleto' and not self.boleto:
            raise ValidationError({'boleto':'Você não incluiu um boleto de pagamento'})
        

        if self.status_pagamento == 'Pago' or self.status_pagamento == 'Reembolsado' or self.status_pagamento == 'Cancelado':
            self.data_pagamento = datetime.date.today()
        else:
            self.data_pagamento = ''

    def __str__(self):
        return f'{self.paciente}: {self.data_emissao}'
    
from typing import Iterable
from django.db import models
from django.core.exceptions import ValidationError
from .const import STATUS_DEPENDENCE_CHOICE
from django.contrib.auth.models import User


# Create your models here.
class Paciente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
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

class Prontuario(models.Model):
    paciente = models.OneToOneField(Paciente, on_delete=models.CASCADE)
    nome = models.CharField(max_length=256)
    peso = models.DecimalField(max_digits= 5, decimal_places= 2 )
    tamanho = models.DecimalField(max_digits=3 , decimal_places= 2)
    alergia = models.BooleanField()
    doenca = models.BooleanField()
    fuma = models.BooleanField()
    bebe = models.BooleanField()
    uso_drogas = models.BooleanField()
    observacoes = models.TextField(null=True)


    
    def __str__(self):
        return self.paciente.name
    
class Documentos(models.Model):
    prontuario = models.OneToOneField(Prontuario, on_delete= models.CASCADE)
    nome_documento = models.CharField(max_length=256)
    descricao = models.TextField(null=True)
    file_documento = models.FileField(upload_to='exames/')


    def __str__(self):
        return self.nome_documento



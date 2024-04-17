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

    
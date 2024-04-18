from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Medico(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  
    data_nascimento = models.DateField(auto_created=False, auto_now=False, auto_now_add=False)
    rg = models.CharField(max_length=9)
    cpf = models.CharField(max_length=11)
    crm = models.CharField(max_length=12)
    telefone = models.CharField(max_length=14)
    cep = models.CharField(max_length=8)
    endereco = models.TextField()
    numero = models.CharField(max_length=10)
    complemento = models.TextField(blank=True, null=True)

    
    
    def __str__(self):
        return self.user.username
    
class Especialidade(models.Model):
    nome_especialidade = models.CharField(max_length=256)


from django.db import models
from django.contrib.auth.models import User
from clinica.models import Especialidade

# Create your models here.
class Medico(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=256, unique=True)
    sexo = models.CharField(max_length=25, choices=(('Masculino', 'Masculino'), ('Feminino', 'Feminino'), ('Outro', 'Outro')))
    genero = models.CharField(max_length=256)  
    data_nascimento = models.DateField(auto_created=False, auto_now=False, auto_now_add=False)
    rg = models.CharField(max_length=9, unique=True)
    cpf = models.CharField(max_length=11, unique=True)
    crm = models.CharField(max_length=12, unique=True)
    especialidade = models.ForeignKey(Especialidade, on_delete=models.CASCADE)
    telefone = models.CharField(max_length=14)
    cep = models.CharField(max_length=8)
    endereco = models.TextField()
    numero = models.CharField(max_length=10)
    complemento = models.TextField(blank=True, null=True)

    
    
    def __str__(self):
        return self.user.username
    



from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Recepcionista(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=256, unique=True)
    sexo = models.CharField(max_length=256, choices=(('Masculino', 'Masculino'), ('Feminino', 'Feminino'), ('Prefiro Não Dizer', 'Prefiro Não Dizer')))
    genero = models.CharField(max_length=256, choices=(('Homem Cis', 'Homem Cis'), ('Mulher Cis', 'Mulher Cis'), ('Homem Trans', 'Homem Trans'), ('Mulher Trans', 'Mulher Trans'), ('Outro', 'Outro'), ('Prefiro Não Dizer', 'Prefiro Não Dizer')))
    data_nascimento = models.DateField(auto_created=False, auto_now=False, auto_now_add=False)
    rg = models.CharField(max_length=9, unique=True)
    cpf = models.CharField(max_length=11, unique=True)
    telefone = models.CharField(max_length=14)
    cep = models.CharField(max_length=8)
    endereco = models.TextField()
    numero = models.CharField(max_length=10)
    complemento = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.user.username

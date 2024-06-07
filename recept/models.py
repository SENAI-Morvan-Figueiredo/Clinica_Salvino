from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import Group

# Create your models here.
class Recepcionista(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=256, unique=True)
    sexo = models.CharField(max_length=256, choices=(('Masculino', 'Masculino'), ('Feminino', 'Feminino'), ('Prefiro Não Dizer', 'Prefiro Não Dizer')))
    genero = models.CharField(max_length=256, choices=(('Homem Cis', 'Homem Cis'), ('Mulher Cis', 'Mulher Cis'), ('Homem Trans', 'Homem Trans'), ('Mulher Trans', 'Mulher Trans'), ('Outro', 'Outro'), ('Prefiro Não Dizer', 'Prefiro Não Dizer')))
    outro = models.CharField(max_length=256, null=True, blank=True)
    data_nascimento = models.DateField(auto_created=False, auto_now=False, auto_now_add=False)
    rg = models.CharField(max_length=9, unique=True)
    cpf = models.CharField(max_length=11, unique=True)
    telefone = models.CharField(max_length=14)
    cep = models.CharField(max_length=8)
    estado = models.CharField(max_length=2)
    cidade = models.CharField(max_length=256)
    bairro = models.CharField(max_length=256)
    logradouro = models.CharField(max_length=512)
    numero = models.CharField(max_length=10)
    complemento = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        grupo, created = Group.objects.get_or_create(name='Recepcionista')
        self.user.groups.add(grupo)

    def __str__(self):
        return self.user.username
    
    def __str__(self):
        return self.user.username

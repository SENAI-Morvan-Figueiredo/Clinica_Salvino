from django.db import models

# Create your models here.

class Convenio(models.Model):
    name = models.CharField(max_length=256, unique=True)

    def __str__(self):
        return self.name
    
class PlanoConvenio(models.Model):
    convenio = models.ForeignKey(Convenio, on_delete=models.CASCADE)
    name = models.CharField(max_length=256, unique=True)

    def __str__(self):
        return self.name
    
class BandeiraCartao(models.Model):
    name = models.CharField(max_length=256, unique=True)

    def __str__(self):
        return self.name
    
class Pix(models.Model):
    nome_proprietario_pix = models.CharField(max_length=256)
    chave = models.CharField(max_length= 256)

    def __str__(self):
        return self.nome_proprietario_pix
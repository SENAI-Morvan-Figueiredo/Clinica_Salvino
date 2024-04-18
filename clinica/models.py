from django.db import models

# Create your models here.
class Convenio(models.Model):
    name = models.CharField(max_length=256, unique=True)

class Tratamento(models.Model):
    name = models.CharField(max_length=256, unique=True)
    preco = models.DecimalField(max_digits=5, decimal_places=2)
    descricao = models.TextField()

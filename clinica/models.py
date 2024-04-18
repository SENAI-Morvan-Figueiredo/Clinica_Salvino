from django.db import models

# Create your models here.
class Especialidade(models.Model):
    nome_especialidade = models.CharField(max_length=256)
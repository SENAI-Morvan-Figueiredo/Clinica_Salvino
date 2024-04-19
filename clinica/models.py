from django.db import models
from paciente.models import Paciente
from medico.models import Medico

# Create your models here.
class Especialidade(models.Model):
    nome_especialidade = models.CharField(max_length=256)

    def __str__(self):
        return self.nome_especialidade
    

class Consulta(models.Model):
    paciente = models.OneToOneField(Paciente,on_delete=models.CASCADE)
    medico = models.OneToOneField(Medico,on_delete=models.CASCADE)
    data = models.DateField(auto_created=False, auto_now=False, auto_now_add=False)
    hora = models.TimeField(auto_created=False, auto_now=False, auto_now_add=False)
    especialidade = models.OneToOneField(Especialidade,on_delete=models.CASCADE)
    status_consulta =models.CharField(max_length=256, choices=(('Concluida','Concluida'), ('Cancelada','Cancelada'), ('Agendada','Agendada'),('Em andamento','Em andamento')))

    def __str__(self):
        return f'{self.paciente.name}  - {self.data}/{self.hora}'
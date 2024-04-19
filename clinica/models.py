from django.db import models
from paciente.models import Paciente
from medico.models import Medico, Especialidade

# Create your models here.

class Consulta(models.Model):
    paciente = models.OneToOneField(Paciente,on_delete=models.CASCADE)
    tipo_consulta = models.CharField(max_length=256, choices=(('Presencial', 'Presencial'), ('Remoto', 'Remoto')))
    medico = models.OneToOneField(Medico,on_delete=models.CASCADE)
    data = models.DateField(auto_created=False, auto_now=False, auto_now_add=False)
    hora = models.TimeField(auto_created=False, auto_now=False, auto_now_add=False)
    especialidade = models.OneToOneField(Especialidade,on_delete=models.CASCADE)
    status_consulta =models.CharField(max_length=256, choices=(('Concluida','Concluida'), ('Cancelada','Cancelada'), ('Agendada','Agendada'),('Em andamento','Em andamento')))

    def __str__(self):
        return f'{self.paciente.name}  - {self.data}/{self.hora}'

class Convenio(models.Model):
    name = models.CharField(max_length=256, unique=True)

    def __str__(self):
        return self.name

class Tratamento(models.Model):
    name = models.CharField(max_length=256, unique=True)
    preco = models.DecimalField(max_digits=6, decimal_places=2)
    descricao = models.TextField()

    def __str__(self):
        return self.name

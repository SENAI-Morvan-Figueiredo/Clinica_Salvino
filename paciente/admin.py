from django.contrib import admin
from .models import Paciente, Prontuario,Documentos


# Register your models here.
admin.site.register(Paciente)
admin.site.register(Prontuario)
admin.site.register(Documentos)

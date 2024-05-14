from django.contrib import admin
from .models import Medico, Tratamento, Especialidade

# Register your models here.
admin.site.register(Medico)
admin.site.register(Especialidade)
admin.site.register(Tratamento)
